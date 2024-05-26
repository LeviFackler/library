import sqlite3
import requests
from bs4 import BeautifulSoup
import json



#conn = sqlite3.connect('books.db')

#cursor = conn.cursor()

#cursor.execute('''CREATE TABLE books (title TEXT, author TEXT, year INTEGER)''')

#conn.commit()
#conn.close()

isbn = input("Enter ISBN: ")

r = requests.get(f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json")
data = r.text
json_object = json.loads(data)
#json_formated_str = json.dumps(json_object, indent=2)
#print(json_formated_str)

# Extract information
book_info = json_object[f"ISBN:{isbn}"]
title = book_info["title"]
subtitle = book_info.get("subtitle", "")
author = book_info["authors"][0]["name"]
publisher = book_info["publishers"][0]["name"]
number_of_pages = book_info.get("number_of_pages", None)  # Default value if key is missing
weight = book_info.get("weight", None)  # Default value if key is missing

# Extract identifiers
identifiers = book_info.get("identifiers", {})
isbn_13 = identifiers.get("isbn_13", [None])[0]
openlibrary_id = identifiers.get("openlibrary", [None])[0]

# Extract classifications
classifications = book_info.get("classifications", {})
lc_classifications = classifications.get("lc_classifications", [None])[0]



# Print extracted information
print("Title:", title)
print("Subtitle:", subtitle)
print("Author:", author)
print("Publisher:", publisher)
print("Number of Pages:", number_of_pages)
print("Weight:", weight)
print("ISBN-13:", isbn_13)
print("OpenLibrary ID:", openlibrary_id)
print("LC Classifications:", lc_classifications)

