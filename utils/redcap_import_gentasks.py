# %%
import pandas as pd
import subjectid_to_seqid as s2s
import os
import sys
import requests
from tkinter import filedialog

# %%
def concatenate_summaries(summaries_path: str) -> pd.DataFrame:
    df = pd.DataFrame()
    for file in os.listdir(summaries_path):
        if file.endswith('.csv'):
            summary = pd.read_csv(os.path.join(summaries_path, file))
            df = pd.concat([df, summary], ignore_index=True)
    return df 
# %%
def prepare_choose_import_file(choose_df: pd.DataFrame) -> pd.DataFrame:
    rename_dict = {
        "subject": "subjectid",
        "experiment": "redcap_repeat_instrument",
        "date": "choose_doadmin",
        "train_accuracy": "choosetrainingaccavg",
        "train_avg_rt": "choosetrainingrtavg",
        "train_errors": "choosetrainingnerr",
        "probe_accuracy": "chooseprobeaccavg",
        "probe_avg_rt": "chooseprobertavg",
        "probe_errors": "chooseprobenerr",
    }
    choose_df = choose_df.rename(columns=rename_dict)
    choose_df["redcap_repeat_instrument"] = "choose_task"
    choose_df["seqid"] = choose_df["subjectid"].apply(s2s.get_seqid)
    choose_df["redcap_repeat_instance"] = choose_df["subjectid"].apply(s2s.get_instance_number)
    choose_df["choose_doadmin"] = choose_df["choose_doadmin"].str.strip("\"")
    choose_df["choose_doadmin"] = pd.to_datetime(choose_df["choose_doadmin"])
    choose_df["choose_doadmin"] = choose_df["choose_doadmin"].dt.strftime("%m/%d/%Y")
    choose_df["choose_task_complete"] = "1" # For unverified data
    choose_df["choosetrainingnerr"] = choose_df["choosetrainingnerr"].astype(int)
    choose_df["chooseprobenerr"] = choose_df["chooseprobenerr"].astype(int)

    for index, row in choose_df.iterrows():
        if pd.isnull(row["seqid"]):
            print(f"Couldn't generate SeqID for subject {row['subjectid']}. Skipping...")

    choose_df = choose_df.dropna(subset=["seqid", "redcap_repeat_instance"], how="any")

    redcap_cols = ["seqid","redcap_repeat_instance", "redcap_repeat_instrument", "choose_doadmin", 
                   "choosetrainingaccavg","choosetrainingrtavg", "choosetrainingnerr", 
                   "chooseprobeaccavg", "chooseprobertavg", "chooseprobenerr", "choose_task_complete"]
    
    choose_df = choose_df.astype(str)
    
    return choose_df[redcap_cols]


# %%
def prepare_fish_import_file(fish_df: pd.DataFrame) -> pd.DataFrame:
    rename_dict = {
        "subject": "subjectid",
        "experiment": "redcap_repeat_instrument",
        "date": "fish_doadmin",
        "acquisition": "facquisition",
        "acquisition_trials": "facquisition_trials",
        "retention": "fretention",
        "generalization": "fgen",
        }
    fish_df = fish_df.rename(columns=rename_dict)
    fish_df["redcap_repeat_instrument"] = "fish_task"
    fish_df["seqid"] = fish_df["subjectid"].apply(s2s.get_seqid)
    fish_df["redcap_repeat_instance"] = fish_df["subjectid"].apply(s2s.get_instance_number)
    fish_df["fish_doadmin"] = fish_df["fish_doadmin"].str.strip("\"")
    fish_df["fish_doadmin"] = pd.to_datetime(fish_df["fish_doadmin"])
    fish_df["fish_doadmin"] = fish_df["fish_doadmin"].dt.strftime("%m/%d/%Y")
    fish_df["fish_task_complete"] = "1" # For unverified data
    fish_df["facquisition_trials"] = fish_df["facquisition_trials"].astype(str)

    for index, row in fish_df.iterrows():
        if pd.isnull(row["seqid"]):
            print(f"Couldn't generate SeqID for {row['subjectid']}. Skipping...")

    fish_df = fish_df.dropna(subset=["seqid", "redcap_repeat_instance"], how="any")

    redcap_cols = ["seqid","redcap_repeat_instance", "redcap_repeat_instrument", "fish_doadmin", 
                   "facquisition","facquisition_trials", "fretention", "fgen", "fish_task_complete"]
    
    fish_df = fish_df.astype(str)
    
    return fish_df[redcap_cols]

# %%
def fetch_summaries_paths(task_path) -> list[str]:
    summaries_paths = []
    for root, dirs, files in os.walk(task_path):
        for dir in dirs:
            if dir == "summaries":
                summaries_paths.append(os.path.join(root, dir))
    return summaries_paths

# %%
def prepare_redcap_import() -> pd.DataFrame:
    utils_path = os.path.dirname(os.path.abspath(__file__))
    tasks_paths = [os.path.join(utils_path, "..", "choose34"),
                   os.path.join(utils_path, "..", "choose_fmri"), 
                   os.path.join(utils_path, "..", "fish15")]
    data_frames = []
    for path in tasks_paths:
        summaries_paths = fetch_summaries_paths(path)
        for summaries_path in summaries_paths:
            if "choose" in path:
                choose_concat = concatenate_summaries(summaries_path)
                choose_df = prepare_choose_import_file(choose_concat)
                data_frames.append(choose_df)
            elif "fish" in path:
                fish_concat = concatenate_summaries(summaries_path)
                fish_df = prepare_fish_import_file(fish_concat)
                data_frames.append(fish_df)
    redcap_import = pd.concat(data_frames, ignore_index=True)
    # make all columns strings
    redcap_import = redcap_import.astype(str)
    return redcap_import

# %%
def redcap_export_records(api_token: str, records: list[str], fields: list[str]) -> requests.Response:
    fields.remove("redcap_repeat_instance")
    fields.remove("redcap_repeat_instrument")
    url = "https://redcap.rutgers.edu/api/"
    data = {
        "token": api_token,
        "content": "record",
        "format": "json",
        "type": "flat",
        "csvDelimiter": "",
        "records": ",".join(records),
        "fields": ",".join(fields),
        "rawOrLabel": "raw",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "false",
        "exportDataAccessGroups": "false",
        "returnFormat": "json"
    }
    print("Requesting data from REDCap...") 
    response = requests.post(url, data=data)
    return response

def redcap_import_records(api_token: str, redcap_import: pd.DataFrame) -> requests.Response:
    url = "https://redcap.rutgers.edu/api/"
    data = {
        "token": api_token,
        "content": "record",
        "format": "json",
        "type": "flat",
        "overwriteBehavior": "normal",
        "data": redcap_import.to_json(orient="records"),
        "dateFormat": "MDY",
        "returnContent": "count",
        "returnFormat": "json"
    }
    response = requests.post(url, data=data)
    return response

# %%
def compare_and_fill(redcap_import: pd.DataFrame, redcap_data: pd.DataFrame) -> pd.DataFrame:
    new_redcap_import = redcap_import.copy()
    for i, row in new_redcap_import.iterrows():
        seqid = row["seqid"]
        instance = row["redcap_repeat_instance"]
        instrument = row["redcap_repeat_instrument"]
        redcap_data_row = redcap_data[(redcap_data["seqid"] == seqid) & (redcap_data["redcap_repeat_instance"] == instance) & (redcap_data["redcap_repeat_instrument"] == instrument)]
        if not redcap_data_row.empty:
            for field in redcap_data_row.columns[3:]:
                if field in new_redcap_import.columns and pd.notnull(redcap_data_row[field].values[0]):
                    new_redcap_import.at[i, field] = str(redcap_data_row[field].values[0])
    return new_redcap_import
            

# %%
def main():
    redcap_import = prepare_redcap_import()
    api_token = None
    if(len(sys.argv) > 1):
        api_token = sys.argv[1]
    else:
        api_token = input("Enter REDCap API token: ")
    
    redcap_export_response = redcap_export_records(api_token, redcap_import["seqid"].unique().tolist(), redcap_import.columns.tolist())
    if(redcap_export_response.status_code != 200):
        print("Error fetching data from REDCap. Exiting...")
        print(redcap_export_response.text)
        sys.exit()

    redcap_data = pd.DataFrame(redcap_export_response.json())
    redcap_data = redcap_data.replace({-9: None, -9.0: None, "-9": None, "-9.0": None})

    redcap_import = compare_and_fill(redcap_import, redcap_data)
    # convert nan to empty string. This way REDCap will ignore NA fields
    redcap_import = redcap_import.replace({"nan": ""})

    print("Choose where to save the REDCap import file...")  
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        redcap_import.to_csv(file_path, index=False)
        print(f"REDCap import file saved to {file_path}")
    else:
        print("No location selected. Exiting...")
        sys.exit()

    redcap_import_response = redcap_import_records(api_token, redcap_import)
    if(redcap_import_response.status_code != 200):
        print("Error importing data to REDCap. Exiting...")
        print(redcap_import_response.text)
        sys.exit()
    print("Data imported successfully to REDCap. Records imported: ", redcap_import_response.json()["count"])

# %%
if __name__ == "__main__":
    main()