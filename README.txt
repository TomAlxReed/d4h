Simple script designed to filter by candidates that meet the required standard,
then convert the .csv output from Google forms to a format that D4h understands.

Inputs: 
    filename.csv - Name of the Google forms generated input file
    uploadDate   - Cutoff date from which to generate the pass list. Used to
                   prevent multiple uploads for the same person.
                  
Outputs:
    filename_d4h.csv - Output file ready to be uploaded to d4h
    
Dependencies:
    Python 3.x https://www.python.org/downloads/

Requirements:
    One column header containing 'Timestamp'
    One column header containing 'Candidate HANTSAR Callsign'
    One column header containing 'Has the candidate passed this assessment?'
    
Known weaknesses:
    No commas ',' allowed anywhere in the .csv file