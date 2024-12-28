from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

# Database setup
def create_db():
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
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

create_db()

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()

    # Fetch all flashcards
    cursor.execute("SELECT * FROM flashcards")
    flashcards = cursor.fetchall()

    # Calculate statistics
    today = datetime.now().date()
    cursor.execute("SELECT COUNT(*) FROM flashcards")
    total_flashcards = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM flashcards WHERE last_reviewed = ?", (today,))
    reviewed_today = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM flashcards WHERE next_review <= ?", (today,))
    due_today = cursor.fetchone()[0]

    stats = {
        "total_flashcards": total_flashcards,
        "reviewed_today": reviewed_today,
        "due_today": due_today
    }

    conn.close()
    return render_template('index.html', flashcards=flashcards, stats=stats)

@app.route('/add_flashcard', methods=['POST'])
def add_flashcard():
    word = request.form['word']
    translation = request.form['translation']

    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flashcards (word, translation, next_review)
        VALUES (?, ?, ?)
    ''', (word, translation, datetime.now().date()))
    conn.commit()
    conn.close()

    flash('Flashcard added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_flashcard', methods=['POST'])
def delete_flashcard():
    flashcard_id = request.form['flashcard_id']

    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
    conn.commit()
    conn.close()

    flash('Flashcard deleted successfully.', 'warning')
    return redirect(url_for('index'))

@app.route('/review_flashcard', methods=['POST'])
def review_flashcard():
    flashcard_id = request.form['flashcard_id']
    remembered = request.form['remembered']
    today = datetime.now().date()

    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()

    if remembered == "yes":
        cursor.execute("SELECT next_review, interval FROM flashcards WHERE id = ?", (flashcard_id,))
        flashcard = cursor.fetchone()
        next_review = flashcard[0]
        interval = flashcard[1]

        if next_review:
            next_date = datetime.strptime(next_review, "%Y-%m-%d").date()
            new_interval = max(1, interval * 2)
        else:
            new_interval = 1  # Start with 1 day

        next_review_date = today + timedelta(days=new_interval)
    else:
        next_review_date = today + timedelta(days=1)

    cursor.execute('''
        UPDATE flashcards
        SET last_reviewed = ?, next_review = ?, interval = ?
        WHERE id = ?
    ''', (today, next_review_date, new_interval, flashcard_id))

    conn.commit()
    conn.close()

    flash('Flashcard reviewed successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/edit_flashcard/<int:flashcard_id>', methods=['GET', 'POST'])
def edit_flashcard(flashcard_id):
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        word = request.form['word']
        translation = request.form['translation']
        cursor.execute('''
            UPDATE flashcards
            SET word = ?, translation = ?
            WHERE id = ?
        ''', (word, translation, flashcard_id))
        conn.commit()
        conn.close()

        flash('Flashcard updated successfully!', 'info')
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM flashcards WHERE id = ?", (flashcard_id,))
        flashcard = cursor.fetchone()
        conn.close()
        return render_template('edit.html', flashcard=flashcard)

if __name__ == '__main__':
    app.run(debug=True)
