# scraper.py

import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
OUTPUT_FILE = "data/books.csv"

def fetch_books_from_page(page_num):
    url = BASE_URL.format(page_num)
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    books = soup.find_all("article", class_="product_pod")
    data = []

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.replace("£", "")
        data.append((title, price))

    return data

def scrape_books(pages=3):
    all_books = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        books = fetch_books_from_page(page)
        all_books.extend(books)
        time.sleep(1)  # Be nice to the server

    # Save to CSV
    with open(OUTPUT_FILE, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price"])
        writer.writerows(all_books)

    print(f"Saved {len(all_books)} books to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_books(pages=5)
