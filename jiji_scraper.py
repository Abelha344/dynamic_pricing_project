import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Configure Chrome to run without a window (Headless)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def collect_ai_data():
    print("🌐 Starting Browser... Preparing to collect Ethiopian market data.")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # We'll scrape the first page of mobile phones
    url = "https://jiji.com.et/mobile-phones"
    driver.get(url)
    
    # Wait for the JavaScript to finish loading the prices
    print("⏳ Waiting for page elements to render...")
    time.sleep(8) 
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    data = []
    # Search for the product containers
    listings = soup.find_all('div', class_=lambda x: x and 'b-list-advert-base' in x)

    for item in listings:
        try:
            # Get Product Name
            title = item.find(class_=lambda x: x and 'title' in x.lower()).text.strip()
            
            # Get Price
            price_text = item.find(string=lambda t: "ETB" in t)
            
            if title and price_text:
                # Clean the price string to a raw integer (AI needs numbers!)
                price_num = int(price_text.replace("ETB", "").replace(",", "").strip())
                data.append({"product_name": title, "price": price_num})
        except:
            continue

    if data:
        df = pd.DataFrame(data)
        df.to_csv("market_data.csv", index=False)
        print(f"✅ SUCCESS: Saved {len(df)} items to 'market_data.csv'")
    else:
        print("❌ FAILED: No data found. Check your internet or Jiji URL.")

if __name__ == "__main__":
    collect_ai_data()