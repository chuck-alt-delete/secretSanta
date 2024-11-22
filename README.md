# Secret Santa

This program assigns secret santas and emails everyone who they have.  Each person has a "noSanta" list of people for whom they can't be secret santa. For example, you might not want to allow spouses to have each other for secret santa. In our house, you can't have your spouse and you can't have the same person you had last year.

For more info about sending emails with python, see http://naelshiab.com/tutorial-send-email-python/. Also note that gmail requires you to create an application specific password for authentication. Go to https://myaccount.google.com/apppasswords and create an application password for this app.

## Instructions

0. Clone this repo.
1. Install python requirements with `python3 -m pip install -r requirements.txt`
1. Create a gmail API key and create a file called `santaDataSecrets` that looks like:
    ```
    email=myemail@gmail.com
    password=myapikey
    ```
1. Initialize your `data/santa.db` database with `./initialize_db.sh`
2. Keep `santaDataSecrets` and `data/santa.db` locally and back up in secure storage (dropbox, lastpass, bitwarden, etc.).
4. Run the application and open to http://localhost:5001:
    ```bash
    python3 app.py
    ```
1. Use the website to view past assignments, create this year's assignments, and email your family with their assignments.
5. Don't peek at your outbox (until next year when you have to make a new santaData json file)!
