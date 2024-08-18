import json
import sqlite3
import sys
import re

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('data/santa.db')
cursor = conn.cursor()

# Check if filename is provided as an argument
if len(sys.argv) != 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

# Get the filename from the command-line arguments
filename = sys.argv[1]

# Extract the year from the filename using a regular expression
match = re.search(r'\d{4}', filename)
if not match:
    print("Error: Year not found in filename.")
    sys.exit(1)

year = int(match.group())

# Load JSON data from file
with open(filename, 'r') as file:
    data = json.load(file)

# Insert data into the Users table
for user in data.values():
    cursor.execute('''
        INSERT OR IGNORE INTO Users (id, name, email)
        VALUES (?, ?, ?)
    ''', (user['id'], user['name'], user['email']))

# Create a name-to-id mapping from the Users table
cursor.execute('SELECT id, name FROM Users')
user_name_to_id_map = {name: id for id, name in cursor.fetchall()}

# Insert data into the Users table
for user in data.values():
    cursor.execute('''
        INSERT OR IGNORE INTO Users (id, name, email)
        VALUES (?, ?, ?)
    ''', (user['id'], user['name'], user['email']))

# If necessary, insert restrictions or assignments
for user in data.values():
    user_id = user['id']
    
    # Insert restrictions (if any)
    for restricted_user_name in user['noSanta']:
        cursor.execute('''
            INSERT OR IGNORE INTO UserRestrictions (user_id, restricted_user_id, year)
            VALUES (?, ?, ?)
        ''', (user_id, user_name_to_id_map[restricted_user_name], year))
    
    # Insert last year’s Secret Santa assignments (if any)
    if user['lastYear'] != 'None':
        last_year_giftee_name = user['lastYear']
        last_year_giftee_id = user_name_to_id_map.get(last_year_giftee_name)
        if last_year_giftee_id is not None:
            cursor.execute('''
                INSERT OR IGNORE INTO SecretSantaAssignments (gifter_id, giftee_id, year)
                VALUES (?, ?, ?)
            ''', (user_id, last_year_giftee_id, year - 1))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data imported successfully.")

