import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import random
import json

class AmazonScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
        }
        
    def get_product_data(self, url):
        """
        Scrape product data from Amazon product page
        """
        try:
            # Add random delay to avoid being blocked
            time.sleep(random.uniform(2, 5))
            
            # Update headers with new random user agent
            self.headers['User-Agent'] = self.ua.random
            
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Failed to fetch the page. Status code: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product data
            product_data = {
                'title': self._get_title(soup),
                'price': self._get_price(soup),
                'rating': self._get_rating(soup),
                'review_count': self._get_review_count(soup),
                'availability': self._get_availability(soup),
                'description': self._get_description(soup),
            }
            
            return product_data
            
        except Exception as e:
            print(f"Error occurred while scraping: {str(e)}")
            return None
    
    def _get_title(self, soup):
        try:
            # Try multiple possible selectors for title
            title = soup.find('span', {'id': 'productTitle'}) or \
                   soup.find('h1', {'id': 'title'}) or \
                   soup.find('span', {'class': 'a-size-large product-title-word-break'})
            return title.text.strip() if title else "N/A"
        except:
            return "N/A"
    
    def _get_price(self, soup):
        try:
            # Try multiple possible selectors for price
            price = soup.find('span', {'class': 'a-price-whole'}) or \
                   soup.find('span', {'class': 'a-offscreen'}) or \
                   soup.find('span', {'class': 'a-price'})
            return price.text.strip() if price else "N/A"
        except:
            return "N/A"
    
    def _get_rating(self, soup):
        try:
            # Try multiple possible selectors for rating
            rating = soup.find('span', {'class': 'a-icon-alt'}) or \
                    soup.find('i', {'class': 'a-icon-star'}) or \
                    soup.find('span', {'class': 'a-icon a-icon-star'})
            if rating:
                rating_text = rating.text.strip()
                if 'out of' in rating_text:
                    return rating_text.split('out of')[0].strip()
                return rating_text
            return "N/A"
        except:
            return "N/A"
    
    def _get_review_count(self, soup):
        try:
            # Try multiple possible selectors for review count
            review_count = soup.find('span', {'id': 'acrCustomerReviewText'}) or \
                          soup.find('span', {'class': 'a-size-base'}) or \
                          soup.find('span', {'class': 'a-size-base s-underline-text'})
            if review_count:
                count_text = review_count.text.strip()
                if 'ratings' in count_text:
                    return count_text.split('ratings')[0].strip()
                return count_text
            return "N/A"
        except:
            return "N/A"
    
    def _get_availability(self, soup):
        try:
            # Try multiple possible selectors for availability
            availability = soup.find('span', {'class': 'a-size-medium a-color-success'}) or \
                          soup.find('span', {'class': 'a-size-medium a-color-price'}) or \
                          soup.find('div', {'id': 'availability'})
            return availability.text.strip() if availability else "N/A"
        except:
            return "N/A"
    
    def _get_description(self, soup):
        try:
            # Try multiple possible selectors for description
            description = soup.find('div', {'id': 'productDescription'}) or \
                         soup.find('div', {'id': 'feature-bullets'}) or \
                         soup.find('div', {'id': 'aplus'})
            return description.text.strip() if description else "N/A"
        except:
            return "N/A"
    
    def save_to_csv(self, data, filename='amazon_products.csv'):
        """
        Save scraped data to CSV file
        """
        df = pd.DataFrame([data])
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    
    def save_to_json(self, data, filename='amazon_products.json'):
        """
        Save scraped data to JSON file
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")

def main():
    # Example usage
    scraper = AmazonScraper()
    
    # Example Amazon product URL
    product_url = input("Enter Amazon product URL: ")
    
    # Scrape product data
    product_data = scraper.get_product_data(product_url)
    
    if product_data:
        # Save data to both CSV and JSON
        scraper.save_to_csv(product_data)
        scraper.save_to_json(product_data)
        
        # Print the scraped data
        print("\nScraped Product Data:")
        for key, value in product_data.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main() 