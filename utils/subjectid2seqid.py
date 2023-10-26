import sys
import os

def seqid_from_longitudinal_subject(subjectid):
    '''
    Subject ID -> SeqID conversion have the following format: 
        AA###   ->  A### (instance 1)
        AA_R### ->  A### (instance 2)
        AA_3R### -> A### (instance 3)
        AA_4R### -> A### (instance 4)
        AA_5R### -> A### (instance 5)
    '''
    seqid = None
    instance_no = None

    # Ex: AAL_3R001 AAL_4R001, AAL_5R001

    seqid = "L" + subjectid[-3:] # L + last 3 digits of subject id

    instance_info = subjectid.split("_")
    if(len(instance_info) > 1):
        instance_info = instance_info[1] # AAL_3R001 -> 3R001
    else: # Invalid subject id
        return None, None

    if(instance_info[0].isdigit() and instance_info[1] == "R"): 
        # instances 3, 4, 5. Ex: 3R001 4R001, 5R001
        instance_no = int(instance_info[0])

    elif(instance_info[0] == "R"):
        # instance 2. Ex: R001
        instance_no = 2

    else:
        # instance 1. Ex: 001 (no R in instance info)
        instance_no = 1

    return seqid, instance_no

def seqid_from_exercise_subject(subjectid):
    '''
    Subject ID -> SeqID conversion have the following format:
        AA###       -> A### (instance 1)
        AA_R###     -> A### (instance 2)
        AA_R###_L   -> A### (instance 3)
        AA_3R###_L  -> A### (instance 4)
        AA_4R###_L  -> A### (instance 5)
        AA_5R###_L  -> A### (instance 6)
    '''
    seqid = None
    instance_no = None

    instance_info = subjectid.split("_")

    if(len(instance_info) > 2):
        # Subject id is something like AA_R001_L
        instance_info = instance_info[1] # AA_R001_L -> R001
        seqid = "A" + instance_info[-3:] # A + last 3 digits of instance info

        if(instance_info[0] == "R"):
            instance_no = 3
        else:
            # instance info is 3R001, 4R001, 5R001
            instance_no = int(instance_info[0]) + 1
    
    elif(len(instance_info) > 1):
        # then subject id is something like AA_R001
        instance_no = 2
        seqid = "A" + subjectid[-3:] # A + last 3 digits of subject id

    else:
        # then subject id is something like AA001
        seqid = "A" + subjectid[-3:] # A + last 3 digits of subject id
        instance_no = 1
    return seqid, instance_no

def seqid_from_new_subject(subjectid):
    '''
    Subject ID -> SeqID conversion have the following format:
        COV###      -> C### (instance 1)
        COV_R###    -> C### (instance 2)
        COV_3R###   -> C### (instance 3)
    '''
    seqid = None
    instance_no = None

    seqid = "C" + subjectid[-3:] # C + last 3 digits of subject id

    instance_info = subjectid.split("_")

    if(len(instance_info) > 1):
        instance_info = instance_info[1]
        if(instance_info[0] == "R"):
            instance_no = 2
        else:
            instance_no = int(instance_info[0])
    else:
        instance_no = 1

    return seqid, instance_no

def get_seqid_and_instance(subjectid):
    '''
    Converts subject id to seqid and instance number.

    Args:
        subjectid (str): Subject ID
    Returns:
        seqid (str): SeqID
        instance_no (int): Instance number
    '''
    seqid = None
    instance_no = None
 
    if(subjectid[:3] == "AAL"): # Longitudinal participant
        seqid, instance_no = seqid_from_longitudinal_subject(subjectid)


    elif(subjectid[:2] == "AA"): # Exercise participant
        seqid, instance_no = seqid_from_exercise_subject(subjectid)



    elif(subjectid[:3] == "COV"): # New participant
        seqid, instance_no = seqid_from_new_subject(subjectid)
    
    return seqid, instance_no

def menu():
    print("Subject ID to SeqID converter")
    response = None
    while(response != "exit"):
        response = input("\nTo exit enter 'exit'\nEnter subject ID(s): ")
        subjectids = response.split(" ")

        for subjectid in subjectids:
            if(subjectid == "exit"):
                break

            seqid, instance_no = get_seqid_and_instance(subjectid)
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
        try:
            with open(sys.argv[2], "r") as f:
                for line in f:
                    subjectids.append(line.strip())
        except:
            print("Error reading file.")
            return
        
        for subjectid in subjectids:
            seqid, instance_no = get_seqid_and_instance(subjectid)
            if(seqid != None and instance_no != None):
                seqids.append((seqid, instance_no))
            else:
                print("Invalid subject ID: " + subjectid)
        try:
            # open file for writing in same directory as input file
            path = os.path.dirname(os.path.abspath(sys.argv[2]))
            csv_path = os.path.join(path, "SeqIDs.csv")
            
            with open(csv_path, "w", newline="") as csv_file:
                csv_file.write("SubjectID,SeqID,Instance\n")
                for i in range(len(subjectids)):
                    csv_file.write(subjectids[i] + "," + seqids[i][0] + "," + str(seqids[i][1]) + "\n")
        except:
            print("Error writing to file. Outputting to console instead.")
            for i in range(len(subjectids)):
                print(subjectids[i] + "," + seqids[i][0] + "," + str(seqids[i][1]))
            return
    else:
        print("Usage: python subjectid2seqid.py [-f <file>]")
        print("Interactive mode: python subjectid2seqid.py")
        print("In interactive mode you will be prompted to enter one or many subject IDs separated by spaces")
        print("The output will be printed to the console/n")
        print("File mode: python subjectid2seqid.py -f <file>")
        print("The file input for file mode is a text file with each line containing a subject ID")
        print("The output will be a CSV file named SeqIDs.csv in the same directory as the input file")


if(__name__ == "__main__"):
    main()