import sqlite3

# Connect to the database (creates a new one if it doesn't exist)
conn = sqlite3.connect("santa.db")

# Create a cursor object
cursor = conn.cursor()

# Create a table for books
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        year INTEGER
    )
""")

# Insert data into the table
cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", ("The Great Gatsby", "F. Scott Fitzgerald", 1925))

# Commit changes to the database
conn.commit()

# Close the database connection
conn.close()

