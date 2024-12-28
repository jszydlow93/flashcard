import sqlite3

# Connect to the database
conn = sqlite3.connect('flashcards.db')
cursor = conn.cursor()

# Add new columns for last_reviewed, next_review, and interval (if not already present)
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        translation TEXT NOT NULL,
        last_reviewed DATE DEFAULT NULL,
        next_review DATE DEFAULT NULL,
        interval INTEGER DEFAULT 1
    );
''')

conn.commit()
conn.close()

print("Database setup completed successfully.")
