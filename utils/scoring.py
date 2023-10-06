import csv

def score_fish_81a(input_file, output_file, errors_file):
    """
    Reads in a Fish 8.1a file and writes the summary information to the output file.

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
            errorfile.write(f"Warning: {input_file} has no generalization trials.\n")
    else:
        info["generalization"] /= info["generalization_trials"]

    # Write to file
    with open(output_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([val for val in info.values()])

    return

def score_choose_321(input_file, output_file, errors_file):
    """
    Reads in a Choose 32.1 file and writes the summary information to the output file.

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

        print(f"Warning: {input_file} has no train trials.")
        with open(errors_file, "a") as errorfile:
            errorfile.write(f"warning: {input_file} has no train trials.\n")
        
    else:
        info["train_accuracy"] /= info["train_trials"]
        info["train_rt_avg"] /= info["train_trials"]


    if(not info["probe_trials"] > 0):
        info["probe_accuracy"] = None
        info["probe_rt_avg"] = None 

        print(f"Warning: {input_file} has no probe trials.")
        with open(errors_file, "a") as errorfile:
            errorfile.write(f"Warning: {input_file} has no probe trials.\n")
    else:
        info["probe_accuracy"] /= info["probe_trials"]
        info["probe_rt_avg"] /= info["probe_trials"]

    # Write to file
    with open(output_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([val for val in info.values()]) 
    
    return