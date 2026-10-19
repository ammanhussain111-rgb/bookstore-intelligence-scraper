"""
The Bookstore Intelligence Mission - reusable scraper for https://books.toscrape.com/

Scrapes ALL catalogue pages (BOSS LEVEL) using one reusable function and a loop,
and saves competitor_books.csv with: Title, Price, Rating, Availability, URL.
"""
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/"
FIRST_PAGE = "https://books.toscrape.com/catalogue/page-1.html"

# The site stores ratings as words in the class: <p class="star-rating Three">
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_page(html, page_url):
    """Extract every book on one catalogue page into a list of dicts."""
    soup = BeautifulSoup(html, "html.parser")
    records = []
    for card in soup.find_all("article", class_="product_pod"):
        link = card.h3.a
        title = link["title"]                                  # full title (text is truncated)
        price = float(card.find("p", class_="price_color").text.replace("£", "").replace("Â", "").strip())
        rating_word = card.find("p", class_="star-rating")["class"][1]
        availability = card.find("p", class_="instock availability").text.strip()
        url = urljoin(page_url, link["href"])
        records.append(
            {
                "Title": title,
                "Price": price,
                "Rating": RATING_MAP[rating_word],
                "Availability": availability,
                "URL": url,
            }
        )
    next_btn = soup.find("li", class_="next")
    next_url = urljoin(page_url, next_btn.a["href"]) if next_btn else None
    return records, next_url


def scrape(max_pages=None, delay=0.2):
    """Follow the 'next' button until the end (or max_pages). Same logic for any page count."""
    all_records, url, n = [], FIRST_PAGE, 0
    session = requests.Session()
    while url and (max_pages is None or n < max_pages):
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        records, url = parse_page(resp.text, resp.url)
        all_records.extend(records)
        n += 1
        print(f"Scraped page {n}: {len(records)} books")
        time.sleep(delay)
    return pd.DataFrame(all_records)


if __name__ == "__main__":
    df = scrape()                       # scrape(max_pages=3) for the base mission, scrape(5) for bonus 1
    df.to_csv("competitor_books.csv", index=False)
    print(df.head())
    print(df.dtypes)
    print(f"Saved {len(df)} rows to competitor_books.csv")
