import sqlite3
import requests
import json
import apiKeys
import dbManage

#GLOBAL VARIABLE
KEY = apiKeys.API_KEY


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


def main():
    dbManage.create_table()
    total_books = 0
    while True:
        isbn = input("Enter ISBN (or type 'exit' to quit): ")

        # Check if the user wants to exit
        if isbn.lower() == 'exit' or isbn.lower() == 'quit':
            print("Exiting program...")
            dbManage.view_data()
            break
        h = {'Authorization': KEY}
        r = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers=h)
        if r.status_code == 200:
            data = r.text
            json_object = json.loads(data)
            extracted_data = extract_info(json_object)
            dbManage.insert_data(extracted_data)
            total_books += 1
            print(f"Total books fetched: {total_books}")
        else:
            print("Error occurred while fetching book data. Please try again.")


if __name__ == "__main__":
    main()