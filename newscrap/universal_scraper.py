import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import random
import json
import logging
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SelectorConfig:
    """Configuration for CSS selectors and data extraction"""
    title: List[str]
    price: List[str]
    rating: List[str]
    review_count: List[str]
    availability: List[str]
    description: List[str]
    custom_fields: Dict[str, List[str]] = None

class UniversalScraper:
    def __init__(self, 
                 base_url: str,
                 selectors: SelectorConfig,
                 delay_range: tuple = (2, 5),
                 max_retries: int = 3):
        """
        Initialize the universal scraper
        
        Args:
            base_url: Base URL of the website
            selectors: SelectorConfig object containing CSS selectors
            delay_range: Tuple of (min, max) delay between requests
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url
        self.selectors = selectors
        self.delay_range = delay_range
        self.max_retries = max_retries
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
    def _make_request(self, url: str) -> Optional[BeautifulSoup]:
        """Make HTTP request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                time.sleep(random.uniform(*self.delay_range))
                self.headers['User-Agent'] = self.ua.random
                
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                
                return BeautifulSoup(response.content, 'html.parser')
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
                    return None
                time.sleep(random.uniform(5, 10))  # Longer delay between retries
    
    def _extract_text(self, soup: BeautifulSoup, selectors: List[str]) -> str:
        """Extract text using multiple possible selectors"""
        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    return element.text.strip()
            except Exception as e:
                logger.debug(f"Failed to extract using selector {selector}: {str(e)}")
        return "N/A"
    
    def scrape_page(self, url: str) -> Optional[Dict]:
        """Scrape data from a single page"""
        if not url.startswith(self.base_url):
            logger.warning(f"URL {url} does not match base URL {self.base_url}")
            return None
            
        soup = self._make_request(url)
        if not soup:
            return None
            
        data = {
            'title': self._extract_text(soup, self.selectors.title),
            'price': self._extract_text(soup, self.selectors.price),
            'rating': self._extract_text(soup, self.selectors.rating),
            'review_count': self._extract_text(soup, self.selectors.review_count),
            'availability': self._extract_text(soup, self.selectors.availability),
            'description': self._extract_text(soup, self.selectors.description),
        }
        
        # Extract custom fields if configured
        if self.selectors.custom_fields:
            for field, selectors in self.selectors.custom_fields.items():
                data[field] = self._extract_text(soup, selectors)
                
        return data
    
    def save_data(self, data: Union[Dict, List[Dict]], 
                 filename: str, 
                 format: str = 'csv') -> None:
        """Save scraped data to file"""
        try:
            if format.lower() == 'csv':
                df = pd.DataFrame([data] if isinstance(data, dict) else data)
                df.to_csv(filename, index=False)
            elif format.lower() == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
            else:
                raise ValueError(f"Unsupported format: {format}")
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save data: {str(e)}")

def main():
    # Example configuration for Amazon
    amazon_selectors = SelectorConfig(
        title=['#productTitle', 'h1#title', '.product-title-word-break'],
        price=['.a-price-whole', '.a-offscreen', '.a-price'],
        rating=['.a-icon-alt', '.a-icon-star', '.a-icon.a-icon-star'],
        review_count=['#acrCustomerReviewText', '.a-size-base', '.a-size-base.s-underline-text'],
        availability=['.a-size-medium.a-color-success', '.a-size-medium.a-color-price', '#availability'],
        description=['#productDescription', '#feature-bullets', '#aplus'],
        custom_fields={
            'brand': ['.po-brand .a-span9', '#bylineInfo', '.a-link-normal.contributorNameID']
        }
    )
    
    # Create scraper instance
    scraper = UniversalScraper(
        base_url='https://www.amazon.com',
        selectors=amazon_selectors
    )
    
    # Get URL from user
    url = input("Enter product URL: ")
    
    # Scrape data
    data = scraper.scrape_page(url)
    
    if data:
        # Save in both formats
        scraper.save_data(data, 'product_data.csv', 'csv')
        scraper.save_data(data, 'product_data.json', 'json')
        
        # Print results
        print("\nScraped Data:")
        for key, value in data.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main() 