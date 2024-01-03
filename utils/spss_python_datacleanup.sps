* Encoding: UTF-8.
* Attempt 1 on Making REDCap Data Export Cleanup *

*Open terminal, get the pathway for the bin folder of contents for SPSS statistics, then set cd to the bin folder there*

*cd /Applications/IBM\ SPSS\ Statistics/SPSS\ Statistics.app/Contents/bin *

*Need to install pandas:  ./statisticspython3 -m pip install numpy scipy pandas openpyxl pyreadstat*


BEGIN PROGRAM PYTHON3

import pandas as pd

# This function fixes the instance issue from REDCap reports by dropping the "redcap_repeat_instrument" column 
# Input 1 = "~path/generatedfilename.csv" 
# Input 2 = "preferredfilename.csv" 

def clean_report(csv, csv_out):

    #Read the REDCap report in as csv 
    
    df=pd.read_csv(csv, delimiter = ",")

    # Drop redcap_repeat_instrument 
    
    df = df.drop('redcap_repeat_instrument', axis=1)
    
    # Fix up the dataset, this concatenates the rows 
    
    df = df.groupby(['seqid', 'redcap_repeat_instance']).first().reset_index()

    # Writes a CSV file with the name you preferred, csv_out 
    
    df.to_csv(csv_out, index=False)
    
    return
    
END PROGRAM


* IGNORE, THESE ARE DRAFT INSTRUCTIONS FOR LATER *

* Uncomment the line below and input your command as clean_report("REDCAP EXPORT NAME.csv", "PREFERRED TITLE FOR EXPORT") *

*show directory
cd Desktop
cd REDCap
cd data_cleanup_spss    
cd data*

* Set your working directory by uncommenting the line below and pasting your filepath next to "cd" which stands for change directory*

* cd Macintosh HD/users/labbie/Downloads_replacethisfilepath*

BEGIN PROGRAM PYTHON3

report = "<filepath>/nameofreport.csv"
output = "<filepath>/titlethecleanedupreport.csv"
clean_report(report, output)

END PROGRAM

