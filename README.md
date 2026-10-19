# bookstore-intelligence-scraper
# Bookstore Intelligence Scraper

Scrapes all 1,000 books from https://books.toscrape.com/ (a practice site)
using requests + BeautifulSoup and saves them to a Pandas DataFrame / CSV.

## Files
- scraper.py: scrapes all 50 pages with one reusable function and a loop
- analysis.py: answers the business questions, solves the £100 challenge, makes the chart
- competitor_books.csv: dataset produced by the scraper
- rating_counts.png: bar chart of books per star rating

## How to run
pip install requests beautifulsoup4 pandas matplotlib
python scraper.py
python analysis.py

## Key finding
Price barely differs by rating (5-star avg £35.37 vs 1-star £34.56),
so highly rated books can be stocked cheaply.
