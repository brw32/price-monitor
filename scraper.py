import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

# File paths
OUTPUT_CSV = "data/books.csv"
OUTPUT_PNG = "data/books_preview.png"
os.makedirs("data", exist_ok=True)

def scrape_books():
    books = []
    for page in range(1, 3):  # You can increase range for more pages
        url = f"http://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(url)

        # Explicitly decode as UTF-8
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        for article in articles:
            title = article.h3.a["title"]
            price = article.find("p", class_="price_color").text.strip()

            # Keep the '£' symbol as-is (this is the correct pound symbol)
            books.append((title, price))
    
    return books

def save_csv(books):
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price"])
        writer.writerows(books)

def save_preview_image():
    df = pd.read_csv(OUTPUT_CSV, encoding="utf-8-sig")
    df = df.head(10)  # Display top 10 for readability

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='left')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    plt.savefig(OUTPUT_PNG, bbox_inches='tight', dpi=200)
    plt.close()

def main():
    books = scrape_books()
    save_csv(books)
    save_preview_image()
    print(f"✅ Scraped {len(books)} books and saved to:")
    print(f"   • CSV: {OUTPUT_CSV}")
    print(f"   • PNG: {OUTPUT_PNG}")

if __name__ == "__main__":
    main()
