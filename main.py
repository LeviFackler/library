import sqlite3
import requests
from bs4 import BeautifulSoup
import json


def create_table():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE books (
                    title TEXT, 
                    subtitle TEXT, 
                    author TEXT, 
                    publisher TEXT, 
                    number_of_pages INTEGER, 
                    weight INTEGER, 
                    publish_date INTEGER, 
                    isbn_13 INTEGER, 
                    openlibrary_id TEXT, 
                    lc_classifications TEXT)''')
    conn.commit()
    conn.close()
#json_formated_str = json.dumps(json_object, indent=2)
#print(json_formated_str)

def insert_data(title, subtitle, author, publisher, number_of_pages, weight, publish_date, isbn_13, openlibrary_id, lc_classifications):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (title, subtitle, author, publisher, number_of_pages, weight, publish_date, isbn_13, openlibrary_id, lc_classifications))
    conn.commit()
    print("Data inserted successfully!")
    conn.close()


def extract_info(json_object, isbn):
    book_info = json_object[f"ISBN:{isbn}"]
    title = book_info["title"]
    subtitle = book_info.get("subtitle", "")
    author = book_info["authors"][0]["name"]
    publisher = book_info["publishers"][0]["name"]
    number_of_pages = book_info.get("number_of_pages", None)  # Default value if key is missing
    weight = book_info.get("weight", None)  # Default value if key is missing
    publish_date = book_info.get("publish_date", None)

    # Extract identifiers
    identifiers = book_info.get("identifiers", {})
    isbn_13 = identifiers.get("isbn_13", [None])[0]
    openlibrary_id = identifiers.get("openlibrary", [None])[0]

    # Extract classifications
    classifications = book_info.get("classifications", {})
    lc_classifications = classifications.get("lc_classifications", [None])[0]

    return title, subtitle, author, publisher, number_of_pages, weight, publish_date, isbn_13, openlibrary_id, lc_classifications

def print_info(title, subtitle, author, publisher, number_of_pages, weight, publish_date, isbn_13, openlibrary_id, lc_classifications):
    print("Title:", title)
    print("Subtitle:", subtitle)
    print("Author:", author)
    print("Publisher:", publisher)
    print("Number of Pages:", number_of_pages)
    print("Weight:", weight)
    print("Publish Date:", publish_date)
    print("ISBN-13:", isbn_13)
    print("OpenLibrary ID:", openlibrary_id)
    print("LC Classifications:", lc_classifications)

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
    while True:
        isbn = input("Enter ISBN (or type 'exit' to quit): ")

        # Check if the user wants to exit
        if isbn.lower() == 'exit' or isbn.lower() == 'quit':
            print("Exiting program...")
            view_data()
            break

        r = requests.get(f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json")
        if r.status_code == 200:
            data = r.text
            json_object = json.loads(data)
            if f"ISBN:{isbn}" in json_object:
                title, subtitle, author, publisher, number_of_pages, weight, publish_date, isbn_13, openlibrary_id, lc_classifications = extract_info(
                    json_object, isbn)
                insert_data(title, subtitle, author, publisher, number_of_pages, weight, publish_date, isbn_13,
                            openlibrary_id, lc_classifications)
                print_info(title, subtitle, author, publisher, number_of_pages, weight, publish_date, isbn_13,
                           openlibrary_id, lc_classifications)
            else:
                print("Book with given ISBN not found.")
        else:
            print("Error occurred while fetching book data. Please try again.")


if __name__ == "__main__":
    main()