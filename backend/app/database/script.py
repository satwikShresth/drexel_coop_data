import csv
import sqlite3

# Path to the CSV file
file_path = './uscities.csv'

# Connect to the SQLite database (or create it)
conn = sqlite3.connect('./uscities.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS uscities (
    city TEXT,
    state_id TEXT
)
''')

# Open the CSV file and read it
with open(file_path, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)

    # Skip the header row
    next(csvreader)

    # Insert rows into the database
    for row in csvreader:
        city = row[0]       # Assuming 'city' is the first column
        state_id = row[2]   # Assuming 'state_id' is the second column
        cursor.execute(
            'INSERT INTO uscities (city, state_id) VALUES (?, ?)', (city, state_id))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Selected data has been successfully imported into the uscities table in the uscities.db database.")
