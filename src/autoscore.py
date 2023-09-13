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
import shutil

##########################################################################
# Can change these imports to use different functions to score the files #
##########################################################################
from scoring import score_fish_81a as score_fish
from scoring import score_choose_321 as score_choose

def main():

    # Check if a path for data files has been specified
    files_path = None

    if len(sys.argv) > 1:
        files_path = sys.argv[1]
    else:
        print("No path for data files has been specified. To specify a path, run the script with the following command:", file=sys.stderr)
        print("\npython scoreFishChoose.py <DATA PATH> \n", file=sys.stderr)
        exit(1)

    ##########################
    # Initialize errors file #
    ##########################
    errors_file = initialize_errors_file(files_path)

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

    organize_errors(errors_file)

def organize_errors(errors_file):
    """
    Organizes the errors file by removing duplicate lines and sorting the lines alphabetically.

    Args:
        errors_file (str): The path to the errors file.
    Returns:
        None
    """
    with open(errors_file, "r") as errorfile:
        lines = errorfile.readlines()
        lines.sort()
    with open(errors_file, "w") as errorfile:
        errorfile.writelines(lines)
    return

def initialize_errors_file(files_path):
    """
    Clears the errors file if it exists, if not it creates it.
    
    Args:
        files_path (str): The path to the directory containing the files.
    Returns:
        errors_file (str): The path to the errors file.
    """
    errors_path = os.path.join(files_path, "errors")
    os.makedirs(errors_path, exist_ok=True)

    errors_file = os.path.join(errors_path, "errors.txt")

    if (os.path.isfile(errors_file)):
        print(f"WARNING: IF YOU CONTINUE ALL DATA IN {errors_file} WILL BE OVERWRITTEN.")
        answer = input("Continue? [y/n] ")
        if(answer != "y"):
            print("Exiting...")
            exit(0)

    with open(errors_file, "w") as errorfile:
        errorfile.write("")
 
    return errors_file


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
        elif("fish" in csv_filename.lower()):
            score_fish(os.path.join(csv_path, csv_filename), fish_output_file, errors_file)
        else:
            print(f"Warning: {csv_filename} does not have a valid Fish or Choose file name. This file will be skipped.")
            with open(errors_file, "a") as errorfile:
                errorfile.write(f"Warning: {csv_filename} does not have a valid Fish or Choose file name. This file will be skipped.\n")

def initialize_summary_files(choose_output_file, fish_output_file):
    """
    Clears the files if they exist, if not it creates them, and writes the headers to the output files.

    Args:
        choose_output_file (str): The path to the choose output file.
        fish_output_file (str): The path to the fish output file.
    Returns:
        None
    """

    if(os.path.isfile(choose_output_file) or os.path.isfile(fish_output_file)):
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

    if(os.path.isdir(csv_path)):
        print(f"\nWARNING: IF YOU CONTINUE IT IS POSSIBLE SOME DATA IN {csv_path} WILL BE OVERWRITTEN")
        answer = input("Continue? [y/n] ")

        if(answer != "y"):
            print("Exiting...")
            exit(0)

    os.makedirs(csv_path, exist_ok=True)
    os.makedirs(summaries_path, exist_ok=True)

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
        elif(not os.path.isdir(os.path.join(files_path, filename))):
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

if __name__ == "__main__":
    main()