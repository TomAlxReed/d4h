"""

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

"""


def writeHeaders(filename):
    pFile = open(filename, 'w')
    pFile.write('name_or_ref,award_date\n')
    pFile.close()

def addEntry(filename, name_or_ref, award_date):
    pFile = open(filename, 'a')
    pFile.write(name_or_ref)
    pFile.write(',')
    pFile.write(award_date)
    pFile.write('\n')
    pFile.close()
    

def timestampToDate(timestamp):
    timestampArr = timestamp.split('/')
    day = int(timestampArr[0][:2])
    month = int(timestampArr[1][:2])
    year = int(timestampArr[2][:4])
    return day, month, year

def timestampToD4h(timestamp):
    timestampArr = timestamp.split('/')
    day = timestampArr[0][:2]
    month = timestampArr[1][:2]
    year = timestampArr[2][:4]
    return (year + '-' + month + '-' + day)

def isInTheFuture(reference, date):
    if (date[2] > reference[2]):
        return True
    if (date[1] > reference[1]):
        return True
    if (date[0] > reference[0]):
        return True
    return False

readFilename = input("Enter input filename (name.csv): ")

uploadFromStr = input("Enter date to upload from (dd/mm/yyyy): ")
uploadFromDate = timestampToDate(uploadFromStr)
print()
print('Upload from date is: ', uploadFromDate)

writeFilename = readFilename[:-4] + '_d4h.csv'
writeHeaders(writeFilename)

pReadFile = open(readFilename, 'r')

headerStr = pReadFile.readline()
headerArr = headerStr.split(',')

timestampIndex = -1
callsignIndex = -1
passIndex = -1

indexCount = 0
for header in headerArr:
    if ((header == 'Timestamp') or (header == 'Timestamp\n')):
        timestampIndex = indexCount
    if ((header == 'Candidate HANTSAR Callsign') or (header == 'Candidate HANTSAR Callsign\n')):
        callsignIndex = indexCount
    if ((header == 'Has the candidate passed this assessment?') or (header == 'Has the candidate passed this assessment?\n')):
        passIndex = indexCount
    indexCount += 1
    
print('Timestamp index is: ', timestampIndex)
print('Callsign index is: ', callsignIndex)
print('Pass index is: ', passIndex)

entryCount = 0
for lineStr in pReadFile.readlines():
    lineArr = lineStr.split(',')
    
    if ((lineArr[passIndex] == 'Yes') or (lineArr[passIndex] == 'Yes\n')):
        date = timestampToDate(lineArr[timestampIndex])
        if (isInTheFuture(uploadFromDate, date)):
            d4h = timestampToD4h(lineArr[timestampIndex])
            addEntry(writeFilename, lineArr[callsignIndex], d4h)
            entryCount += 1
            
print(entryCount, ' entries added')
