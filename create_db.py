import sqlite3

# Connect to the sqlite database
con = sqlite3.connect('flashcards.db')

# Create cursor object
cursor = con.cursor()

# Create flashcards table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY,
        word TEXT NOT NULL,
        translation TEXT NOT NULL
    )
''')

con.commit()
con.close()

print("Database created and table initialized.")