from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'books.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    books = query_db('SELECT * FROM books')
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        query_db('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = query_db('SELECT * FROM books WHERE id = ?', [book_id], one=True)
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        query_db('UPDATE books SET title = ?, author = ? WHERE id = ?', (title, author, book_id))
        return redirect(url_for('index'))
    return render_template('edit.html', book=book)

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    query_db('DELETE FROM books WHERE id = ?', [book_id])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
