from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'books.db'

# Initialize DB
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

# Helper to query DB
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# CREATE
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    query_db('INSERT INTO books (title, author) VALUES (?, ?)', (data['title'], data['author']))
    return jsonify({'message': 'Book added'}), 201

# READ ALL
@app.route('/books', methods=['GET'])
def get_books():
    books = query_db('SELECT * FROM books')
    return jsonify([{'id': b[0], 'title': b[1], 'author': b[2]} for b in books])

# READ ONE
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = query_db('SELECT * FROM books WHERE id = ?', [book_id], one=True)
    if book:
        return jsonify({'id': book[0], 'title': book[1], 'author': book[2]})
    return jsonify({'error': 'Book not found'}), 404

# UPDATE
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    query_db('UPDATE books SET title = ?, author = ? WHERE id = ?', (data['title'], data['author'], book_id))
    return jsonify({'message': 'Book updated'})

# DELETE
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    query_db('DELETE FROM books WHERE id = ?', [book_id])
    return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)
