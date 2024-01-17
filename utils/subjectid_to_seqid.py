import sys
import os
import re

class SubjectID:
    exercise_pattern = r"^AA(_[3-9]?R)?[0-9]{3}(_L)?$"
    longitudinal_pattern = r"^AAL_([3-9]?R)?[0-9]{3}$"
    new_participant_pattern = r"^COV(_[3-9]?R)?[0-9]{3}$"

    def is_valid(subjectid):
        return re.match(SubjectID.exercise_pattern, subjectid) or re.match(SubjectID.longitudinal_pattern, subjectid) or re.match(SubjectID.new_participant_pattern, subjectid)

def get_instance_number_from_longitudinal_subject(subjectid):
    '''
    Subject ID -> SeqID conversion have the following format: 
        AA###   ->  A### (instance 1)
        AA_R### ->  A### (instance 2)
        AA_3R### -> A### (instance 3)
        AA_4R### -> A### (instance 4)
        AA_5R### -> A### (instance 5)
    '''
    instance_no = None

    instance_info = subjectid.split("_")
    if(len(instance_info) > 1):
        instance_info = instance_info[1] # AAL_3R001 -> 3R001
    else: # Invalid subject id
        return None

    if(instance_info[0].isdigit() and instance_info[1] == "R"): 
        # instances 3, 4, 5. Ex: 3R001 4R001, 5R001
        instance_no = int(instance_info[0])

    elif(instance_info[0] == "R"):
        # instance 2. Ex: R001
        instance_no = 2

    else:
        # instance 1. Ex: 001 (no R in instance info)
        instance_no = 1

    return instance_no

def get_instance_number_from_exercise_subject(subjectid):
    '''
    Subject ID -> SeqID conversion have the following format:
        EX###       -> E### (instance 1)
        AA###       -> A### (instance 1)
        AA_R###     -> A### (instance 2)
        AA_R###_L   -> A### (instance 3)
        AA_3R###_L  -> A### (instance 4)
        AA_4R###_L  -> A### (instance 5)
        AA_5R###_L  -> A### (instance 6)
    '''
    instance_no = None

    instance_info = subjectid.split("_")

    if(len(instance_info) > 2):
        # Subject id is something like AA_R001_L
        instance_info = instance_info[1] # AA_R001_L -> R001

        if(instance_info[0] == "R"):
            instance_no = 3
        else:
            # instance info is 3R001, 4R001, 5R001
            instance_no = int(instance_info[0]) + 1
    
    elif(len(instance_info) > 1):
        # then subject id is something like AA_R001
        instance_no = 2

    else:
        # then subject id is something like AA001
        instance_no = 1
    return instance_no

def get_instance_number_from_new_subject(subjectid):
    '''
    Subject ID -> SeqID conversion have the following format:
        COV###      -> C### (instance 1)
        COV_R###    -> C### (instance 2)
        COV_3R###   -> C### (instance 3)
    '''
    instance_no = None
    instance_info = subjectid.split("_")

    if(len(instance_info) > 1):
        instance_info = instance_info[1]
        if(instance_info[0] == "R"):
            instance_no = 2
        else:
            instance_no = int(instance_info[0])
    else:
        instance_no = 1

    return instance_no

def get_instance_number(subjectid):
    '''
    Gets instance number from subject id.

    Args:
        subjectid (str): Subject ID
    Returns:
        instance_no (int): Instance number
    '''
    instance_no = None

    if(re.match(SubjectID.exercise_pattern, subjectid)):
        instance_no = get_instance_number_from_exercise_subject(subjectid)
    elif(re.match(SubjectID.longitudinal_pattern, subjectid)):
        instance_no = get_instance_number_from_longitudinal_subject(subjectid)
    elif(re.match(SubjectID.new_participant_pattern, subjectid)):
        instance_no = get_instance_number_from_new_subject(subjectid)

    return instance_no

def get_seqid(subjectid):

    seqid = None

    if(SubjectID.is_valid(subjectid)):
        digits = re.search(r"[0-9]{3}", subjectid).group()
        if(re.match(SubjectID.exercise_pattern, subjectid)):
            seqid = "A" + digits
        elif(re.match(SubjectID.longitudinal_pattern, subjectid)):
            seqid = "L" + digits
        elif(re.match(SubjectID.new_participant_pattern, subjectid)):
            seqid = "C" + digits

    return seqid

def get_subjectid(seqid, instance_no):
    '''
    Converts seqid and instance number to subject id.

    Args:
        seqid (str): SeqID
        instance_no (int): Instance number
    Returns:
        subjectid (str): Subject ID
    '''
    subjectid = None

    digits = seqid[1:] # remove first letter from seqid

    if(seqid[0] == "A"): # Exercise participant

        if(instance_no == 1):
            subjectid = "AA" + digits
        elif(instance_no == 2):
            subjectid = "AA_R" + digits
        elif(instance_no == 3):
            subjectid = "AA_R" + digits + "_L"
        else:
            subjectid = "AA_" + str(instance_no - 1) + "R" + digits + "_L"

    elif(seqid[0] == "L"): # Longitudinal participant
        if(instance_no == 1):
            subjectid = "AAL_" + digits
        elif(instance_no == 2):
            subjectid = "AAL_R" + digits
        else:
            subjectid = "AAL_" + str(instance_no) + "R" + digits

    elif(seqid[0] == "C"): # New participant
        if(instance_no == 1):
            subjectid = "COV" + digits
        elif(instance_no == 2):
            subjectid = "COV_R" + digits
        else:
            subjectid = "COV_" + str(instance_no - 1) + "R" + digits
 
    return subjectid

def menu():
    print("Subject ID to SeqID converter")
    response = None
    while(response != "exit"):
        response = input("\nTo exit enter 'exit'\nEnter subject ID(s): ")
        subjectids = response.split(" ")

        for subjectid in subjectids:
            if(subjectid == "exit"):
                break

            seqid = get_seqid(subjectid)
            instance_no = get_instance_number(subjectid)
            if(seqid != None and instance_no != None):
                print("Subject ID: " + subjectid + " -> SeqID: " + seqid + " Instance: " + str(instance_no))
            else:
                print("Invalid subject ID: " + subjectid)

def main():
    if(len(sys.argv) == 1): # Interactive mode
        menu()
    elif(len(sys.argv) == 3 and sys.argv[1] == "-f"): # File mode
        subjectids = []
        seqids = []
        instance_nos = []
        try:
            with open(sys.argv[2], "r") as f:
                for line in f:
                    subjectids.append(line.strip())
        except:
            print("Error reading file.")
            return
        
        for i, subjectid in enumerate(subjectids):
            seqid = get_seqid(subjectid)
            instance_no = get_instance_number(subjectid)
            if(seqid != None and instance_no != None):
                seqids.append(seqid)
                instance_nos.append(instance_no)
            else:
                print("Invalid subject ID: " + subjectid)
                seqids.append("")
                instance_nos.append("")
        try:
            # open file for writing in same directory as input file
            path = os.path.dirname(os.path.abspath(sys.argv[2]))
            csv_path = os.path.join(path, "SeqIDs.csv")
        
            with open(csv_path, "w", newline="") as csv_file:
                csv_file.write("SubjectID,SeqID,Instance\n")
                for i in range(len(subjectids)):
                    csv_file.write(subjectids[i] + "," + str(seqids[i]) + "," + str(instance_nos[i]) + "\n")
        except:
            print("Error writing to file. Outputting to console instead.")
            for i in range(len(subjectids)):
                print(subjectids[i] + "," + str(seqids[i]) + "," + str(instance_nos[i]))
            return
    else:
        print("Usage: python subjectid2seqid.py [-f <file_path>]\n")
        print("Interactive mode: python subjectid2seqid.py")
        print("In interactive mode you will be prompted to enter one or many subject IDs separated by spaces")
        print("The output will be printed to the console\n")
        print("File mode: python subjectid2seqid.py -f <file_path>")
        print("The file input for file mode is a text file with each line containing a subject ID")
        print("The output will be a CSV file named SeqIDs.csv in the same directory as the input file")


if(__name__ == "__main__"):
    main()