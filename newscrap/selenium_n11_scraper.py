from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import time

def get_text_or_na(driver, selectors):
    for selector in selectors:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            if element and element.text.strip():
                return element.text.strip()
        except Exception:
            continue
    return "N/A"

def main():
    url = "https://www.n11.com/urun/skechers-microspec-ii-zovrix-buyuk-erkek-cocuk-siyah-spor-ayakkabi-403924l-bksr-58372693?magaza=pointspor"

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--lang=tr-TR')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(5)  # Wait for page to load

    data = {
        'title': get_text_or_na(driver, ['h1.proName', '.productName', 'h1.name']),
        'price': get_text_or_na(driver, ['ins[content]', '.newPrice ins', '.newPrice', '.price']),
        'rating': get_text_or_na(driver, ['span.rating', '.ratingValue']),
        'review_count': get_text_or_na(driver, ['.ratingCount', '.reviewCount']),
        'availability': get_text_or_na(driver, ['.stockStatus', '.stockInfo']),
        'description': get_text_or_na(driver, ['.productDescription', '.description', '.product-detail-description', '.product-detail-content']),
        'seller': get_text_or_na(driver, ['.sellerName', '.merchantName']),
        'brand': get_text_or_na(driver, ['a.colorR50', '.brand', '.productBrand']),
        'category': get_text_or_na(driver, ['.breadcrumb', '.categoryPath'])
    }

    driver.quit()

    # Save to CSV
    df = pd.DataFrame([data])
    df.to_csv('selenium_n11_product_data.csv', index=False)
    # Save to JSON
    with open('selenium_n11_product_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("\nScraped Product Data:")
    for key, value in data.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main() 