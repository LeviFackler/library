import sqlite3

# Create a table in the database if it doesn't exist
def create_table():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        publisher TEXT,
        language TEXT,
        title_long TEXT,
        weight REAL,
        pages INTEGER,
        date_published INTEGER,
        authors TEXT,
        title TEXT,
        isbn13 TEXT,
        isbn10 TEXT,
        binding TEXT,
        redundant INTEGER DEFAULT 0  -- 0 means not redundant, 1 means redundant
    )
    ''')
    conn.commit()
    conn.close()


def insert_data(extracted_data):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Check if ISBN13 or ISBN10 already exists in the database
    cursor.execute('''
       SELECT * FROM books WHERE isbn13 = ? OR isbn10 = ?
       ''', (extracted_data["isbn13"], extracted_data["isbn10"]))
    existing_entry = cursor.fetchone()

    redundant = 1 if existing_entry else 0

    cursor.execute('''
    INSERT INTO books (publisher, language, title_long, weight, pages, date_published, authors, title, isbn13, isbn10, binding, redundant)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        extracted_data["publisher"],
        extracted_data["language"],
        extracted_data["title_long"],
        extracted_data["weight"],
        extracted_data["pages"],
        extracted_data["date_published"],
        extracted_data["authors"],
        extracted_data["title"],
        extracted_data["isbn13"],
        extracted_data["isbn10"],
        extracted_data["binding"],
        redundant
    ))

    conn.commit()
    print("Data inserted successfully!")
    conn.close()

    # View the data in the database in the terminal
def view_data():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM books''')
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print("No data found in the database.")
    else:
        for row in rows:
            print(row)
