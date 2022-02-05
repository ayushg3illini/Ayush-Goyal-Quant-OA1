import json
import re
import csv 


class EmailFiller :
    userData = []
    noOfColumns = 0
    emailInput = {}
    emailContent = ""
    errorFlag = 0

    def readUserData(self, filename) :
        """ Reads the user email data from the 'filename' csv file"""
        with open(filename, newline='') as dataInputFile:
            self.userData = list( csv.DictReader(dataInputFile) )
        self.noOfColumns = len(self.userData[0])
        for i in range(self.noOfColumns):
            ithColumnName = list(self.userData[0].keys())[0] 
            self.userData[0][ithColumnName.lower()] = self.userData[0].pop(ithColumnName)

    def readEmailInfo(self,filename):
        """ Reads the email destination data from the 'filename' csv file"""
        with open(filename, newline='') as emailDataInputFile:
            self.emailInput = dict( list(csv.DictReader(emailDataInputFile))[0] )

    def readEmailSubjectAndBody(self,filename) :
        """ Reads the user email subject and body data from the 'filename' text file"""
        with open( filename, newline='') as templateFile :
            self.emailContent = templateFile.read()
        subject = re.search(r'Subject: (.*)\n', self.emailContent,re.IGNORECASE )
        emailBody = re.search(r'Subject: .*\n\n((.|\n)*)', self.emailContent,re.IGNORECASE )
        self.emailInput['Subject'] = subject.group(1)
        self.emailInput['body'] = emailBody.group(1) 

    def userInputPattern(self) :
        """ Takes and extract the pattern used for future data replacement in the email templates from user input.
            We are taking the user input for the pattern becuase the encoding of auto detection of a pattern by the
            script may be inefficienct since it may detect an incorrect pattern as the original pattern for replacement.
            It is difficult to predict which combination of characters user might want to consider as the replacement 
            pattern for the email template. 
        """
        patternString = input("Enter replace pattern: ")
        pattern = re.search(r'([^a-zA-Z0-9]*)[a-zA-Z\s]+(.*)', patternString )
        while pattern == None or pattern.group(1) == None or pattern.group(1) == '' or pattern.group(2) == None or pattern.group(2) == '':
            patternString = input("Enter replace pattern again: ")
            pattern = re.search(r'([^a-zA-Z0-9]*)[a-zA-Z\s]+(.*)', patternString , re.IGNORECASE)
        return pattern 

    def fillTemplate(self, pattern) :
        """ Fills the user email tempalte with the user data obtained from csv files"""
        replacedOutput = self.emailInput['body']
        patternPrefix = re.sub(r'([\.\^\$\*\+\-\?\(\)\[\]\{\}\\\|\—\/])', r'\\\1', pattern.group(1) )   # List of all the special meaning characters in regular expression module
        patternPostfix = re.sub(r'([\.\^\$\*\+\-\?\(\)\[\]\{\}\\\|\—\/])', r'\\\1', pattern.group(2) ) 
        replacedOutput = re.sub(r'' + patternPrefix + '(.+)'+ patternPostfix, lambda m: self.userData[0].get(m.group(1).lower()) , replacedOutput ,flags=re.IGNORECASE )
        self.emailInput['body'] = replacedOutput

    def errorDetection(self, pattern) :
        """ Detects errors based on the user specified pattern in the email template"""
        for i in range(self.noOfColumns):
            searchResult = re.search('([^\sa-zA-Z]+)' + list(self.userData[0].keys())[i] + '([^\sa-zA-Z]+)', self.emailInput['body'], re.IGNORECASE)
            if searchResult ==  None:
                continue 
            if searchResult.group(1) != pattern.group(1) or searchResult.group(2) != pattern.group(2) :
                self.errorFlag = 1
        if self.errorFlag == 1 :
            print("There are errors in the drafted Email")
        else:
            print("The drafted email is error free")

    def writeJsonFile(self) :
        """ Writes the collaborated details regarding the user email onto a json file"""
        jsonOutput = json.dumps(self.emailInput)
        textInputFile = open('email_formatted.json', 'r+')   
        json.dump(jsonOutput,textInputFile)
        print("JSON File Updated")
        textInputFile.close()

def main() :
    fillUserEmail = EmailFiller()
    fillUserEmail.readEmailInfo('email_info.csv')
    fillUserEmail.readEmailSubjectAndBody('email_template.txt')
    fillUserEmail.readUserData('user_data.csv')
    pattern = fillUserEmail.userInputPattern()
    fillUserEmail.fillTemplate(pattern)
    fillUserEmail.errorDetection(pattern)
    fillUserEmail.writeJsonFile()

if __name__ == '__main__' :
    main()






    

