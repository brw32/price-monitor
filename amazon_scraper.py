# scraper.py

import requests
from bs4 import BeautifulSoup
import csv
import time

URL = "https://www.amazon.com/Epson-DURABrite-T127120-High-capacity-Cartridge-Black/dp/B003LD5QIE?pd_rd_w=PB3Et&content-id=amzn1.sym.6669831e-9eeb-4d57-9d29-51b7c8f17181&pf_rd_p=6669831e-9eeb-4d57-9d29-51b7c8f17181&pf_rd_r=928SVP86WW6CTEFNPKDB&pd_rd_wg=4zqjV&pd_rd_r=b9372b60-360c-4088-a94c-d336b371778a&pd_rd_i=B003LD5QIE&ref_=pd_bap_d_grid_rp_0_1_ec_pd_hp_d_atf_rp_3_i&th=1"  # Replace with the product's URL
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
OUTPUT_FILE = "data/amazon_price.csv"

def get_amazon_price():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find(id="productTitle")
    price = soup.find("span", class_="a-offscreen")

    if title and price:
        product_title = title.get_text(strip=True)
        product_price = price.get_text(strip=True)
        return product_title, product_price
    else:
        return None, None

def save_to_csv(title, price):
    with open(OUTPUT_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), title, price])

def monitor_once():
    print("Checking price...")
    title, price = get_amazon_price()
    if title and price:
        print(f"{title} - {price}")
        save_to_csv(title, price)
    else:
        print("Failed to fetch price.")

if __name__ == "__main__":
    monitor_once()
