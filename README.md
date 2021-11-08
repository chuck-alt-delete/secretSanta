# Secret Santa

This program assigns secret santas and emails everyone who they have.  Each person has a "noSanta" list of people whom they can't be secret santa for. For example, you might not want to allow spouses to have each other for secret santa. In our house, you can't have your spouse and you can't have the same person you had last year.

For more info about sending emails with python, see http://naelshiab.com/tutorial-send-email-python/. Also note that gmail requires you to create an application specific password for authentication. See your google security settings for more information.

For now, you have to go back to the outbox for last year to update the "lastYear" field for each member of the family. There is a TODO to automatically update the json for next year.

## Instructions

0. Clone this repo.
1. Create a gmail API key and create a file called `santaDataSecrets` that looks like:
    ```
    email=myemail@gmail.com
    password=myapikey
    ```
2. Use the `sampleData.json` as a template to create a json file for your user data (names and emails). By convention, json files that start with `santaData` are ignored in git to protect your users' email addresses from source control. Example: `santaData2021.json`. Keep these secret files locally or in secure storage (dropbox, lastpass, bitwarden, etc.).
3. Edit the `file` and `secrets_file` variables in `secretSanta.py` to point to your user json file (e.g. `santaData2021.josn`) and secrets file (`santaDataSecrets`).
4. Run the python script to send the emails:
    ```bash
    python3 secretSanta.py
    ```
5. Don't peek at your outbox (until next year when you have to make a new santaData json file)!