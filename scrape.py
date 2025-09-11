from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

def scrape_hamrobazar(search_query="samsung mobile"):
    # Create data folder if not exists
    os.makedirs("data", exist_ok=True)

    # Init Chrome
    driver = webdriver.Chrome()
    driver.get("https://hamrobazaar.com/")
    time.sleep(3)  # wait for homepage load

    # --- Search ---
    input_search = driver.find_element(By.NAME, "searchValue")
    search_button = driver.find_element(By.CLASS_NAME, "nav-searchbar-input-searchIcon")

    input_search.send_keys(search_query)
    search_button.click()
    time.sleep(5)  # wait for results load

    #-- Scroll to load more products ---
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(20):  # scroll 20 times
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Scrape product data ---
    titles, prices, locations, descriptions, links = [], [], [], [], []

    product_cards = driver.find_elements(By.CSS_SELECTOR, "div.card-product-linear-info")
    print(f"Found {len(product_cards)} products")

    for card in product_cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "h2.product-title").text
        except:
            title = ""

        try:
            price = card.find_element(By.CSS_SELECTOR, "div.productPrice").text
        except:
            price = ""

        try:
            location = card.find_element(By.CSS_SELECTOR, "span.location").text
        except:
            location = ""

        try:
            description = card.find_element(By.CSS_SELECTOR, "p.description").text
        except:
            description = ""

        try:
            link = card.find_element(By.CSS_SELECTOR, "a.card-link").get_attribute("href")
        except:
            link = ""

        titles.append(title)
        prices.append(price)
        locations.append(location)
        descriptions.append(description)
        links.append(link)

    #-- Save to CSV ---
    driver.quit()
    df = pd.DataFrame({
        "Title": titles,
        "Price": prices,
        "Location": locations,
        "Description": descriptions,
        "Link": links
    })
    df.to_csv("data/hamrobazar_results.csv", index=False, encoding="utf-8-sig")
    print(f"Scraping complete. {len(df)} products saved to data/hamrobazar_results.csv")

if __name__ == "__main__":
    scrape_hamrobazar("samsung mobile")
