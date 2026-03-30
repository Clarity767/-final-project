from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            description TEXT,
            year INTEGER,
            image_url TEXT,
            created_at TEXT,
            is_read INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/author')
def author():
    return render_template('author.html')


@app.route('/library', methods=['GET', 'POST'])
def library():
    conn = get_db_connection()

    if request.method == 'POST':
        title = request.form.get('title')
        author_name = request.form.get('author')
        description = request.form.get('description')
        year = request.form.get('year')
        image_url = request.form.get('image_url')
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            year = int(year)
        except (ValueError, TypeError):
            year = None

        conn.execute(
            '''INSERT INTO books 
            (title, author, description, year, image_url, created_at) 
            VALUES (?, ?, ?, ?, ?, ?)''',
            (title, author_name, description, year, image_url, created_at)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('library'))

    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('library.html', books=books)


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('library'))



@app.route('/mark_read/<int:id>')
def mark_read(id):
    conn = get_db_connection()
    conn.execute('UPDATE books SET is_read = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('library'))

@app.route('/book/<int:id>')
def book_detail(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('book_detail.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)