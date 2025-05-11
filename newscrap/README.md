# Universal Web Scraper

A powerful and flexible web scraping tool that can be configured to scrape data from various websites. Currently supports Amazon, n11.com, and Instagram, with the ability to easily add more websites.

## Features

- Universal scraping architecture that can be adapted for different websites
- Selenium-based scraping for JavaScript-heavy websites
- Instagram profile and post scraping with authentication
- Configurable selectors for different website structures
- Support for multiple data fields
- Data export to both CSV and JSON formats
- Built-in retry mechanism and error handling
- Anti-bot detection measures
- Secure credential storage

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/universal-web-scraper.git
cd universal-web-scraper
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Install Chrome browser if not already installed (required for Selenium)

## Usage

### Instagram Scraper

1. First time setup:
   - Run the script:
   ```bash
   python instagram_scraper.py
   ```
   - Enter your Instagram credentials when prompted
   - They will be saved in `config.json` for future use

2. Subsequent runs:
   - Just run the script and enter the target username to scrape
   - No need to enter credentials again

The scraper will collect:
- Profile information (followers, following, bio, etc.)
- Recent posts (up to 10 by default)
- Save data in both CSV and JSON formats

### Amazon Scraper

```bash
python amazon_scraper.py
```

### n11.com Scraper

```bash
python selenium_n11_scraper.py
```

## Project Structure

```
universal-web-scraper/
├── README.md
├── requirements.txt
├── config.json              # Instagram credentials (not tracked by git)
├── universal_scraper.py     # Base scraper class
├── amazon_scraper.py        # Amazon-specific implementation
├── selenium_n11_scraper.py  # n11.com implementation with Selenium
├── instagram_scraper.py     # Instagram implementation
└── output/                  # Directory for scraped data
    ├── amazon_products.csv
    ├── amazon_products.json
    ├── n11_products.csv
    ├── n11_products.json
    ├── instagram_profiles/
    └── instagram_posts/
```

## Security

- `config.json` contains sensitive credentials and should not be shared
- Add `config.json` to `.gitignore` to prevent accidental commits
- Keep your credentials private

## Requirements

- Python 3.7+
- Chrome browser
- Required Python packages (see requirements.txt)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational purposes only. Please respect websites' terms of service and robots.txt files. Always check if a website allows scraping before using this tool.

## Acknowledgments

- BeautifulSoup4 for HTML parsing
- Selenium for browser automation
- Instaloader for Instagram scraping
- Fake UserAgent for rotating user agents 