import json
import re
import csv 

with open('user_data.csv', newline='') as dataInputFile:
    userData = csv.DictReader(dataInputFile)

noOfColumns = len(userData[0])
for i in range(noOfColumns):
    ithColumnName = userData[0].keys()[i] 
    userData[ithColumnName.lower()] = userData[0].pop(ithColumnName)
    
textInputFile = open('email_file.json', 'r+')  
emailInput = textInputFile.load() 

errorFlag = 0
pattern = re.search(r'(*)[a-zA-Z](*)')
patternString = input("Enter replace pattern: ")
while pattern == None :
    patternString = input("Enter replace pattern again: ")
    pattern = re.search(r'(*)[a-zA-Z](*)', patternString , re.IGNORECASE)

# If this does not work, then run a loop for substitution 
replacedOutput = re.sub(pattern.group(1) + r'(*)' + pattern.group(2), userData[0][ (r'\1').lower() ], emailInput['body'], flags=re.IGNORECASE )

emailInput['body'] = replacedOutput
print(replacedOutput)

for i in range(noOfColumns):
    searchResult = re.search(r'(*)' + userData[0].keys()[i] + r'(*)' , emailInput['body'], re.IGNORECASE)
    if searchResult.group(1) != pattern.group(1) or searchResult.group(1) != pattern.group(2) :
        errorFlag = 1

if errorFlag == 1 :
    print("There are errors in the drafted Email")

jsonOutput = json.dumps(emailInput) 
json.dump(jsonOutput,textInputFile)
textInputFile.close()


    

