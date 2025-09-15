from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

# Chrome options 
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.page_load_strategy = 'eager'

driver_path = r"C:\chromedriver.exe"  #update your path
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
driver.set_page_load_timeout(120)

def scrape_daraz(search_query="Smartphones under 50000", max_pages=6):
    driver.get("https://www.daraz.com.np/")
    time.sleep(3)
    driver.maximize_window()

    # Search box
    search_box = driver.find_element(By.CLASS_NAME, "search-box__input--O34g")
    search_btn = driver.find_element(By.CLASS_NAME, "search-box__button--1oH7")
    search_box.send_keys(search_query)
    search_btn.click()
    time.sleep(5)

    # --- Data lists ---
    titles, prices, solds, ratings, locations, links = [], [], [], [], [], []

    page = 1
    while page <= max_pages:
        print(f"Scraping page {page}...")
        # Scroll to load products
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(1)

        # All products on this page
        products = driver.find_elements(By.CSS_SELECTOR, "div[data-qa-locator='product-item']")

        for p in products:
            try: title = p.find_element(By.CSS_SELECTOR, "div.RfADt").text
            except: title = ""
            try: price = p.find_element(By.CSS_SELECTOR, "div.aBrP0").text
            except: price = ""
            try: sold = p.find_element(By.CSS_SELECTOR, "span._1cEkb").text
            except: sold = ""
            try: rating = p.find_element(By.CSS_SELECTOR, "div.mdmmT._32vUv").text
            except: rating = ""
            try: location = p.find_element(By.CSS_SELECTOR, "span.oa6ri").text
            except: location = ""
            try: link = p.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except: link = ""

            titles.append(title)
            prices.append(price)
            solds.append(sold)
            ratings.append(rating)
            locations.append(location)
            links.append(link)

        # Pagination
        if page < max_pages:
            clicked = False
            next_page_num = page + 1
            try:
                page_link = driver.find_element(By.CSS_SELECTOR, f"ul.ant-pagination li[title='{next_page_num}'] a")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", page_link)
                page_link.click()
                clicked = True
            except:
                pass
            if not clicked:
                try:
                    next_btn = driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-next a")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                    next_btn.click()
                    clicked = True
                except:
                    pass
            if not clicked:
                print("No more pages.")
                break
            time.sleep(3)
        page += 1

    # JSON generation - short questions, specs separate
    qa_list = []
    for i in range(len(titles)):
        full_title = titles[i].strip()
        specs = ""
        if "|" in full_title:
            product_name, specs = full_title.split("|", 1)
            product_name = product_name.strip()
            specs = specs.strip()
        else:
            product_name = full_title
        
        #cleans raw text removes Rs. and commas from price, sold and ratings
        price = prices[i].replace("Rs. ","").replace(",","").strip()
        sold = solds[i].replace(" sold","").strip() if solds[i] else "0"
        rating = ratings[i].replace("(","").replace(")","").strip() if ratings[i] else "0"
        location = locations[i].strip()
        link = links[i].strip()

        qa_list.append({
            "title": product_name,
            "specs": specs,
            "price": price,
            "sold": sold,
            "rating": rating,
            "location": location,
            "link": link,
            "qa": [
                {"question": f"What is the price of {product_name}?", "answer": f"The price of {product_name} is Rs {price}."},
                {"question": f"How many units of {product_name} were sold?", "answer": f"{sold} units of {product_name} were sold."},
                {"question": f"What is the rating of {product_name}?", "answer": f"{product_name} has a rating of {rating}."},
                {"question": f"Give details and link of {product_name}.", "answer": f"{product_name}, sold in {location}. Link: {link}"}
            ]
        })

    # Save JSON
    with open("daraz_qa_clean.json", "w", encoding="utf-8") as f:
        json.dump(qa_list, f, indent=2, ensure_ascii=False)

    print("Scraping completed")
    driver.quit()

# Run scraper
if __name__ == "__main__":
    scrape_daraz("Smartphones under 50000", max_pages=6)
