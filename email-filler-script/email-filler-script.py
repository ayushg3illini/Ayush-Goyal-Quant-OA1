import json
import re
import csv 

userData=[]

with open('user_data.csv', newline='') as dataInputFile:
    userData = list( csv.DictReader(dataInputFile) )

noOfColumns = len(userData[0])
for i in range(noOfColumns):
    ithColumnName = list(userData[0].keys())[i] 
    userData[0][ithColumnName.lower()] = userData[0].pop(ithColumnName)

# textInputFile = open('email_file.json', 'r+')  
# emailInput = textInputFile.load() # Refine Input based on email and add files 

emailInput = {}
with open('email_info.csv', newline='') as emailDataInputFile:
    emailInput = dict( list(csv.DictReader(emailDataInputFile))[0] )



emailContent = ""
with open('email_template.txt', newline='') as templateFile :
    emailContent = templateFile.read()

subject = re.search(r'Subject: (.*)\n', emailContent,re.IGNORECASE )
emailBody = re.search(r'Subject: .*\n\n((.|\n)*)', emailContent,re.IGNORECASE )
emailInput['Subject'] = subject.group(1)
# print(subject.group(1))
# print(emailBody.group(1))
emailInput['body'] = emailBody.group(1)



errorFlag = 0
patternString = input("Enter replace pattern: ")
pattern = re.search(r'([^a-zA-Z0-9]*)[a-zA-Z\s]+(.*)', patternString )
while pattern == None or pattern.group(1) == None or pattern.group(1) == '' or pattern.group(2) == None or pattern.group(2) == '':
    patternString = input("Enter replace pattern again: ")
    pattern = re.search(r'([^a-zA-Z0-9]*)[a-zA-Z\s]+(.*)', patternString , re.IGNORECASE)

# print(pattern.group(1))
# print("Div")
# print(pattern.group(2))

# Could be made more efficient = look for sub with dict search using re.compile
replacedOutput = emailInput['body']
# print(replacedOutput)
print(noOfColumns)
for i in range(noOfColumns):
    # print(userData[0][list(userData[0].keys())[i]])
    # print("" + pattern.group(1) + list(userData[0].keys())[i] + pattern.group(2))
    if '[' in pattern.group(1) and ']' in pattern.group(2) :
        patternPrefix = re.sub(r'\[', "\\[", pattern.group(1))
        patternPostfix = re.sub(r'\]', "\\]", pattern.group(2))
    # print(patternPrefix)
    # print(patternPostfix)
    # print(r'' + patternPrefix + list(userData[0].keys())[i] + patternPostfix)
    replacedOutput = re.sub(r'' + patternPrefix + list(userData[0].keys())[i] + patternPostfix, userData[0][list(userData[0].keys())[i]] , replacedOutput , flags=re.IGNORECASE ) 
    # print(replacedOutput)

# print(replacedOutput)
emailInput['body'] = replacedOutput
# print(replacedOutput)

for i in range(noOfColumns):
    print(list(userData[0].keys())[i])
    # print(emailInput['body'])
    searchResult = re.search('([^\sa-zA-Z]+)' + list(userData[0].keys())[i] + '([^\sa-zA-Z]+)', emailInput['body'], re.IGNORECASE)
    # if (searchResult.group(1) != pattern.group(1) and searchResult.group(1) in pattern.group(1)) or (searchResult.group(2) != pattern.group(2) and searchResult.group(2) in pattern.group(2))  :
    #     errorFlag = 1
    # print(searchResult.group(1))
    # print(searchResult.group(2))

    if searchResult ==  None:
        continue 

    if searchResult.group(1) != pattern.group(1) or searchResult.group(2) != pattern.group(2) :
        errorFlag = 1

if errorFlag == 1 :
    print("There are errors in the drafted Email")
else:
    print("The drafted email is error free")

jsonOutput = json.dumps(emailInput)
textInputFile = open('email_formatted.json', 'r+')   
json.dump(jsonOutput,textInputFile)
textInputFile.close()


    

