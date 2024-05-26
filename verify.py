import sqlite3

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

view_data()