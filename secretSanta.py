'''
Input: family data (emails,names, relationship status)
Output: secret santa assignments where married couples can't have each other and you don't get the same person
you got last year

'''
import json
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#### Initialize Variables
file = 'santaData2022.json'
secrets_file = "santaDataSecrets"
# TODO: define output json file for next year's input data


#### Main Function
def main():
    santaData = load_data(file)
    santaDict = assign_santas(santaData)
    # print(santaDict)
    email_assignments(santaData, santaDict, secrets_file)
    # update_json(santaData, santaDict, outputFile.json)

#### Helper Functions
def load_data(file):
    with open(file,'r') as f:
        santaData = json.load(f)
    return santaData


def assign_santas(santaData):
    randlist = list(range(len(santaData)))
    random.shuffle(randlist)

    while not goodlist(randlist, santaData):
        random.shuffle(randlist)

    # assign secret santas
    santaDict = {} # {Gifter: Giftee}
    for index in range(len(randlist)):
        santaDict[santaData[str(index)]["name"]] = santaData[str(randlist[index])]["name"]
    
    return santaDict


def email_assignments(santaData, santaDict, secrets_file):
    """see https://stackabuse.com/how-to-send-emails-with-gmail-using-python/ for more info"""

    # load credentials
    with open(secrets_file, 'r') as secret:
        for line in secret:
            data = line.split('=')
            if data[0] == "email":
                email = data[1].strip()
            if data[0] == "password":
                password = data[1].strip()

    # Log into email server
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email, password)

    # Send emails
    for id in santaData:
        gifter = santaData[id]["name"]
        giftee = santaDict[gifter]
        message = MIMEMultipart()
        message['From'] = email
        message['To'] = santaData[id]["email"]
        message['Subject'] = "Casias Christmas 2022"
        body = f'''
-------------------------------------------------
You: {gifter}
Who you have for Secret Santa Stockings: {giftee}
-------------------------------------------------

Hey {gifter}!

For the seventh year in a row, we are doing Secret Stockings! You get to fill the stocking of {giftee} this year!

We will be celebrating Christmas in Concord on January 1st! Your stocking stuffers
for {giftee} should include at least one item you made yourself. Examples include but are not limited to:
- cookies
- poems
- paintings
- knit hats
- cocktails in a jar
- performances
- vehicles

In addition to your one hand-made item, we recommend you try to support local small businesses, but of course,
do what you gotta do.

Can't wait to celebrate the season together!

Love,
Santa
        '''
        message.attach(MIMEText(body,'plain'))
        text = message.as_string()
        server.sendmail(email, santaData[id]["email"] , text)

    server.quit()


def update_json(file):
    # TODO: create function to take the output santaDict and update the santaData with new
    # entries for "lastYear". Dump the results in json and write to next year's file.
    pass


#### Helper function helper functions

def goodlist(array, santaData):
    '''
    Input: array of ids where index is the id of the gifter and the value is the id of the giftee. 
    Output: True if the array is a "good list", false otherwise.
        The list is called "good" if no person has themselves or anyone they aren't supposed
        to have for secret santa.
    '''
    for gifter_id, giftee_id in enumerate(array):
        if gifter_id == giftee_id:
            return False # You can't have yourself for secret santa
        elif santaData[str(giftee_id)]["name"] in santaData[str(gifter_id)]["noSanta"]:
            return False # can't have someone on your noSanta list
    return True


#### Run main program
if __name__ == "__main__":
    main()