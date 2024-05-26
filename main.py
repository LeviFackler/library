import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import apiKeys

#GLOBAL VARIABLE
KEY = apiKeys.API_KEY


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
        binding TEXT
    )
    ''')

    conn.commit()
    conn.close()


def insert_data(extracted_data):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO books (publisher, language, title_long, weight, pages, date_published, authors, title, isbn13, isbn10, binding)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        extracted_data["binding"]
    ))

    conn.commit()
    print("Data inserted successfully!")
    conn.close()



def extract_info(json_object):
    book_info = json_object["book"]
    extracted_data = {
        "publisher": book_info.get("publisher"),
        "language": book_info.get("language"),
        "title_long": book_info.get("title_long"),
        "weight": book_info.get("dimensions_structured", {}).get("weight", {}).get("value"),
        "pages": book_info.get("pages"),
        "date_published": book_info.get("date_published"),
        "authors": ", ".join(book_info.get("authors")),  # Convert list to a comma-separated string
        "title": book_info.get("title"),
        "isbn13": book_info.get("isbn13"),
        "isbn10": book_info.get("isbn10"),
        "binding": book_info.get("binding")
    }

    #print(json.dumps(extracted_data, indent=2))
    print("Data extracted successfully!")
    return extracted_data


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


def main():
    create_table()
    total_books = 0
    while True:
        isbn = input("Enter ISBN (or type 'exit' to quit): ")

        # Check if the user wants to exit
        if isbn.lower() == 'exit' or isbn.lower() == 'quit':
            print("Exiting program...")
            view_data()
            break
        h = {'Authorization': KEY}
        r = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers=h)
        if r.status_code == 200:
            data = r.text
            json_object = json.loads(data)
            extracted_data = extract_info(json_object)
            insert_data(extracted_data)
            total_books += 1
            print(f"Total books fetched: {total_books}")
        else:
            print("Error occurred while fetching book data. Please try again.")


if __name__ == "__main__":
    main()