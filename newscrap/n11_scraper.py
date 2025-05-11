from universal_scraper import UniversalScraper, SelectorConfig
import requests
from fake_useragent import UserAgent
import time
import random
from bs4 import BeautifulSoup

class N11Scraper(UniversalScraper):
    def __init__(self):
        # Configuration for n11.com
        n11_selectors = SelectorConfig(
            title=['.productName', 'h1.name'],
            price=['.newPrice ins', '.newPrice', '.price'],
            rating=['.rating', '.ratingValue'],
            review_count=['.ratingCount', '.reviewCount'],
            availability=['.stockStatus', '.stockInfo'],
            description=['.productDescription', '.description'],
            custom_fields={
                'seller': ['.sellerName', '.merchantName'],
                'brand': ['.brand', '.productBrand'],
                'category': ['.breadcrumb', '.categoryPath']
            }
        )
        
        super().__init__(
            base_url='https://www.n11.com',
            selectors=n11_selectors,
            delay_range=(5, 10),  # Increased delay
            max_retries=5  # Increased retries
        )
        
        # Create a session for persistent cookies
        self.session = requests.Session()
        
        # More realistic headers
        self.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua.random
        })
        
        # Initialize session with headers
        self.session.headers.update(self.headers)
        
    def _make_request(self, url: str):
        """Override the request method with session support"""
        for attempt in range(self.max_retries):
            try:
                # Random delay between requests
                time.sleep(random.uniform(*self.delay_range))
                
                # Update User-Agent for each request
                self.session.headers['User-Agent'] = self.ua.random
                
                # Make the request
                response = self.session.get(url)
                response.raise_for_status()
                
                return BeautifulSoup(response.content, 'html.parser')
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    print(f"Failed to fetch {url} after {self.max_retries} attempts")
                    return None
                time.sleep(random.uniform(10, 15))  # Longer delay between retries

def main():
    # Create scraper instance
    scraper = N11Scraper()
    
    # URL to scrape
    url = "https://www.n11.com/urun/skechers-microspec-ii-zovrix-buyuk-erkek-cocuk-siyah-spor-ayakkabi-403924l-bksr-58372693?magaza=pointspor"
    
    # Scrape data
    data = scraper.scrape_page(url)
    
    if data:
        # Save in both formats
        scraper.save_data(data, 'n11_product_data.csv', 'csv')
        scraper.save_data(data, 'n11_product_data.json', 'json')
        
        # Print results
        print("\nScraped Product Data:")
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print("Failed to scrape the product data. The website might be blocking our requests.")

if __name__ == "__main__":
    main() 