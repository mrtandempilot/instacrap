# instagram Web Scraper

A powerful web scraping tool that can extract data from multiple websites including Instagram, Amazon, and n11.com.

## Features

- Instagram profile and post scraping
- Amazon product data extraction
- n11.com product scraping
- Secure credential storage
- CSV and JSON export
- Anti-bot detection measures

## Quick Start

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Run Instagram scraper:
```bash
python instagram_scraper.py
```

3. Run Amazon scraper:
```bash
python amazon_scraper.py
```

4. Run n11.com scraper:
```bash
python selenium_n11_scraper.py
```

## Project Structure

```
universal-web-scraper/
├── instagram_scraper.py     # Instagram profile and post scraper
├── amazon_scraper.py        # Amazon product scraper
├── selenium_n11_scraper.py  # n11.com product scraper
├── requirements.txt         # Python dependencies
└── output/                  # Scraped data directory
```

## Requirements

- Python 3.7+
- Chrome browser
- Required packages in requirements.txt

## Note

This tool is for educational purposes only. Please respect websites' terms of service and robots.txt files.
