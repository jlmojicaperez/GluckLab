'''
Author: Jose Mojica Perez

Usage: python scoreFishChoose.py <DATA PATH>



scoreFishChoose.py takes in a directory with Fish8.1a and Choose32.1 
files and outputs summaries of the data in CSV format.
Copyright (C) 2023  Jose Mojica Perez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Author's contact information: 
    email: jmojicaperez@acm.org
'''

# imports
import os
import csv
import sys
import pandas as pd

from shutil import rmtree

def main():

    # Check if a path for data files has been specified
    files_path = None

    if len(sys.argv) > 1:
        files_path = sys.argv[1]
    else:
        print("No path for data files has been specified. To specify a path, run the script with the following command:", file=sys.stderr)
        print("\npython scoreFishChoose.py <DATA PATH> \n", file=sys.stderr)
        exit(1)

    # Initialize errors file
    errors_file = os.path.join(files_path, "errors.txt")
    with open(errors_file, "w") as errorfile:
        errorfile.write("")
    
    ###############################
    # Get the files in files_path #
    ###############################
    excel_files, text_files = get_files(files_path, errors_file)

    ################################################
    # Create subdirectories and output files paths #
    ################################################
    csv_path, choose_output_file, fish_output_file = create_dirs(files_path)

    #######################################
    # Convert excel and text files to csv #
    #######################################
    convert_files_to_csv(files_path, excel_files, text_files, csv_path, errors_file)

    #################################
    # Clear files and write headers #
    #################################
    initialize_summary_files(choose_output_file, fish_output_file)
    
    #################################################################
    # Score all files in csv_path and write results to output files #
    #################################################################
    score_all(csv_path, choose_output_file, fish_output_file, errors_file)

def score_all(csv_path, choose_output_file, fish_output_file, errors_file):
    """
    Scores all the files in the csv_path directory and writes the summary information to the output files.

    Args:
        csv_path (str): The path to the directory containing the csv files.
        choose_output_file (str): The path to the choose output file.
        fish_output_file (str): The path to the fish output file.
    Returns:
        None
    """
    
    csv_filenames = os.listdir(csv_path)

    for csv_filename in csv_filenames:
        if("choose" in csv_filename.lower()):
            score_choose(os.path.join(csv_path, csv_filename), choose_output_file, errors_file)
        else:
            score_fish(os.path.join(csv_path, csv_filename), fish_output_file, errors_file)

def initialize_summary_files(choose_output_file, fish_output_file):
    """
    Clears the files if they exist, if not it creates them, and writes the headers to the output files.

    Args:
        choose_output_file (str): The path to the choose output file.
        fish_output_file (str): The path to the fish output file.
    Returns:
        None
    """

    print(f"\nWARNING: IF YOU CONTINUE ALL DATA IN {choose_output_file} AND {fish_output_file} WILL BE OVERWRITTEN.")
    answer = input("Continue? [y/n] ")

    if(answer != "y"):
        print("Exiting...")
        exit(0)

    header_fields = [    
        "subject",
        "experiment",
        "experimenter",
        "date",
        "time",
        "condition",
        "task",
        "train_accuracy",
        "train_errors",
        "train_rt_avg",
        "train_trials", 
        "probe_accuracy",
        "probe_errors",
        "probe_rt_avg",
        "probe_trials"
    ]
    with open(choose_output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(header_fields)

    header_fields = [
        "subject",
        "experiment",
        "experimenter",
        "date",
        "time",
        "acquisition",
        "acquisition_trials",
        "retention",
        "retention_trials",
        "generalization",
        "generalization_trials"
    ]
    with open(fish_output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(header_fields)

    return

def convert_files_to_csv(files_path, excel_files, text_files, csv_path, errors_file):
    """
    Converts all the excel and text files in files_path to csv files and stores them in csv_path.
    
    Args:
        files_path (str): The path to the directory containing the files.
        excel_files (list): A list of excel files in files_path.
        text_files (list): A list of text files in files_path.
        csv_path (str): The path to the directory where the csv files will be stored.
    Returns:
        None
    """

    ##############################
    # Convert excel files to csv #
    ##############################
    for filename in excel_files:
        file_path = os.path.join(files_path, filename)
        try:
            df = pd.read_excel(file_path)
        except:
            print(f"Error reading {filename}. This file will be skipped.")
            with open(errors_file, "a") as errorfile:
                errorfile.write(f"Error reading {filename}. This file will be skipped.\n")
            continue
        new_filename = "".join(filename.split(".")[:-1]) + ".csv"

        new_path = os.path.join(csv_path, new_filename)
        df.to_csv(new_path, index=False)

    #############################
    # Convert text files to csv #
    #############################

    # Note: These text files are in a non-wellformed TSV format and they are kept in the same format
    # and converted to CSV format by replacing the tabs with commas just so we can score all the 
    # files with the same code.

    for filename in text_files:
        file_path = os.path.join(files_path, filename)
        new_path = os.path.join(csv_path, filename + ".csv")
        with open(file_path, 'r') as f:
            with open(new_path, 'w') as new_f:
                for line in f:
                    new_f.write(line.replace('\t', ','))
    return 

def create_dirs(files_path):
    """
    Creates the csv and summaries subdirectories in files_path and returns the paths to the subdirectories 
    and the output files.
    
    Args:
        files_path (str): The path to the directory containing the files.
    Returns:
        csv_path (str): The path to the csv subdirectory.
        summaries_path (str): The path to the summaries subdirectory.
        choose_output_file (str): The path to the choose output file.
        fish_output_file (str): The path to the fish output file.
    """

    # Making a sub-directory called "csv" which will contain all the fish and choose files 
    # in CSV format and another subdirectory called "summaries" which will contain the 
    # summarized information of all files in CSV format for both experiments

    csv_path = os.path.join(files_path, "csv")
    summaries_path = os.path.join(files_path, "summaries")

    print(f"\nWARNING: IF YOU CONTINUE ALL DATA IN {csv_path} AND {summaries_path} WILL BE OVERWRITTEN")
    answer = input("Continue? [y/n] ")

    if(answer != "y"):
        print("Exiting...")
        exit(0)
    
    # Remove directories and their contents if they already exist
    if(os.path.isdir(csv_path)):
        rmtree(csv_path)
    if(os.path.isdir(summaries_path)):
        rmtree(summaries_path)

    os.makedirs(csv_path)
    os.makedirs(summaries_path)

    choose_output_file = os.path.join(summaries_path,"choose_summary.csv")
    fish_output_file = os.path.join(summaries_path,"fish_summary.csv")

    return csv_path, choose_output_file, fish_output_file

def get_files(files_path, errors_file):
    """
    Returns a list of excel files and a list of text files in files_path.

    Args:
        files_path (str): The path to the directory containing the files.
    Returns:
        excel_files (list): A list of excel files in files_path.
        text_files (list): A list of text files in files_path.
    """
    excel_files = []
    text_files = []
    for filename in os.listdir(files_path):
        if(filename.endswith(".xlsx") or filename.endswith(".xls")):
            excel_files.append(filename)
        elif(not os.path.isdir(os.path.join(files_path, filename)) and filename != "errors.txt"):
            text_files.append(filename)

    if(not (len(excel_files)+ len(text_files)) > 0):
        print(f"No files were detected in {files_path}. Exiting...", file=sys.stderr)
        with open(errors_file, "a") as errorfile:
            errorfile.write(f"No files were detected in {files_path}. Exiting...\n")
        exit(1)
    else:
        print(f"Found {len(excel_files)} excel files in {files_path}")
        print(f"Found {len(text_files)} plain text files in {files_path}")
    
    return excel_files, text_files

def score_fish(input_file, output_file, errors_file):
    """
    Reads in a fish file and writes the summary information to the output file.

    Args:
        input_file (str): The path to the input file.
        output_file (str): The path to the output file.
    Returns:
        None
    """
    info = {
        "subject": None,
        "experiment": None,
        "experimenter": None,
        "date": None,
        "time": None,
        "acquisition": 0.0,
        "acquisition_trials": 0,
        "retention": 0.0,
        "retention_trials": 0,
        "generalization": 0.0,
        "generalization_trials": 0,
    }
    header_info = ["experiment","subject","experimenter","date","time"]
    has_read_header = False
    has_skipped_notes = False
    current_phase = None
    try:
        with open(input_file, 'r') as csvfile:
            for row in csvfile:
                row = row.strip().split(',')

                # Skip empty rows or rows with no data
                if(len(row[0]) == 0 or row[0] == "Trial" or "Note" in row[0]):
                    continue
                # Skip header rows if already read header
                if (not has_read_header):
                    if(info["experiment"] == None):
                        info["experiment"] = row[0]
                        continue
                    elif(info["experimenter"] != None and info["date"] == None):
                        info["date"] = "".join(row[:3]).strip('"').strip()
                        continue
                    for item in header_info:
                        if(info[item] == None and item in row[0].lower()):
                            if("experimenter" in row[0].lower()):
                                info[item] = row[0].split()[1].strip()
                            elif("time" in row[0].lower()):
                                info[item] = ":".join(row[0].split(":")[1:]).strip()
                            else:
                                info[item] = row[0].split(':')[1].strip()
                    has_read_header = True
                    for item in header_info:
                        if(info[item] == None):
                            has_read_header = False
                            break
                    continue
                
                if(not has_skipped_notes and "PHASE" not in row[0]):
                    continue
                else:
                    has_skipped_notes = True

                # Get phase
                if("PHASE 3" in row[0]):
                    current_phase = "retention"
                    continue
                elif("PHASE" in row[0]):
                    current_phase = "acquisition"
                    continue

                # Check for generalization trials
                if("*" in row[7]):
                    info["generalization_trials"] += 1
                    info["generalization"] += float(row[7].strip("*"))
                else: # is either retention or acquisition
                    info[f"{current_phase}_trials"] += 1
                    info[current_phase] += float(row[7])
    except:
        print(f"Error reading {input_file}. This file will be skipped.")
        with open(errors_file, "a") as errorfile:
            errorfile.write(f"Error reading {input_file}. This file will be skipped.\n")
        return
    
    # Calculate averages
    if(info["acquisition_trials"] == 0):
        
        info["acquisition"] = None

        print(f"Warning: {input_file} has no acquisition trials.")
        with open(errors_file, "a") as errorfile:
            errorfile.write(f"Warning: {input_file} has no acquisition trials.\n")
    else:
        info["acquisition"] /= info["acquisition_trials"]

    if(info["retention_trials"] == 0):

        info["retention"] = None

        print(f"Warning: {input_file} has no retention trials.")
        with open(errors_file, "a") as errorfile:
            errorfile.write(f"Warning: {input_file} has no retention trials.\n")
    else:
        info["retention"] /= info["retention_trials"]

    if(info["generalization_trials"] == 0):

        info["generalization"] = None

        print(f"Warning: {input_file} has no generalization trials.")
        with open(errors_file, "a") as errorfile:
            errorfile.write(f"Warning: {input_file} has no generalization trials.")
    else:
        info["generalization"] /= info["generalization_trials"]

    # Write to file
    with open(output_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([val for val in info.values()])

    return

def score_choose(input_file, output_file, errors_file):
    """
    Reads in a choose file and writes the summary information to the output file.

    Args:
        input_file (str): The path to the input file.
        output_file (str): The path to the output file.
    Returns:
        None
    """
    info = {
        "subject": None,
        "experiment": None,
        "experimenter": None,
        "date": None,
        "time": None,
        "condition": None,
        "task": None,
        "train_accuracy": 0.0,
        "train_errors": 0,
        "train_rt_avg": 0.0,
        "train_trials": 0,
        "probe_accuracy": 0.0,
        "probe_errors": 0,
        "probe_rt_avg": 0.0,
        "probe_trials": 0
    }
    header_info = ["experiment","subject","experimenter","date","time","condition","task"]
    has_read_header = False
    current_phase = None
    try:
        with open(input_file, 'r') as csvfile:
            for row in csvfile:
                row = row.strip().split(',')

                # Skip empty rows or rows with no data
                if(len(row[0]) == 0 or row[0] == "Trial"):
                    continue
                # Skip header rows if already read header
                if (not has_read_header):
                    if(info["experiment"] == None):
                        info["experiment"] = row[0]
                        continue
                    for item in header_info:
                        if(info[item] == None and item in row[0].lower()):
                            if("experimenter" in row[0].lower()):
                                try:
                                    info[item] = row[0].split()[1].strip()
                                except:
                                    info[item] = ""
                            elif("date" in row[0].lower()):
                                info[item] = "".join(row[1:]).strip('"').strip()
                            elif("time" in row[0].lower()):
                                info[item] = ":".join(row[0].split(":")[1:]).strip()
                            else:
                                info[item] = row[0].split(':')[1].strip()
                    has_read_header = True
                    for item in header_info:
                        if(info[item] == None):
                            has_read_header = False
                            break
                    continue

                # Keep track which phase we are on
                if("TRAINING" in row[0]):
                    current_phase = "train"
                    continue
                if("PROBE" in row[0]):
                    current_phase = "probe"
                    continue

                # Read in data and update info
                info[f"{current_phase}_trials"] += 1
                correct = float(row[5])
                if(correct > 0):
                    info[f"{current_phase}_accuracy"] += float(row[5])
                else:
                    info[f"{current_phase}_errors"] += 1
                info[f"{current_phase}_rt_avg"] += float(row[6])
    except:
        print(f"Error reading {input_file}. This file will be skipped.")
        with open(errors_file, "a") as errorfile:
            errorfile.write(f"Error reading {input_file}. This file will be skipped.\n")
        return

    # Calculate averages
    if(not info["train_trials"] > 0):

        info["train_accuracy"] = None
        info["train_rt_avg"] = None

        print(f"WARNING: {input_file} has no train trials.")
        with open(errors_file, "a") as errorfile:
            errorfile.write(f"warning: {input_file} has no train trials.\n")
        
    else:
        info["train_accuracy"] /= info["train_trials"]
        info["train_rt_avg"] /= info["train_trials"]


    if(not info["probe_trials"] > 0):
        info["probe_accuracy"] = None
        info["probe_rt_avg"] = None 

        print(f"WARNING: {input_file} has no probe trials.")
        with open(errors_file, "a") as errorfile:
            errorfile.write(f"WARNING: {input_file} has no probe trials.\n")
    else:
        info["probe_accuracy"] /= info["probe_trials"]
        info["probe_rt_avg"] /= info["probe_trials"]

    # Write to file
    with open(output_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([val for val in info.values()]) 
    
    return

if __name__ == "__main__":
    main()