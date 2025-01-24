"""
Scrape Products data from Amazon
script run on a daily basis
"""

from selenium import webdriver # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from time import sleep
from fake_useragent import UserAgent # type: ignore
import json
import csv
from random import randint
from tqdm import tqdm
from datetime import datetime
from utils.llm_inference import analyse_sentiment

PRODUCTS_LINKS_MAP = {
    "s23": "https://www.amazon.in/Samsung-Galaxy-Ultra-Phantom-Storage/dp/B0BT9FDZ8N/?th=1",
    "whirpool": "https://www.amazon.in/Whirlpool-Fully-Automatic-WHITEMAGIC-ROYAL-7-0/dp/B08QP41KBP/?th=1",
    "ps5": "https://www.amazon.in/Sony-CFI-2008A01X-PlayStation%C2%AE5-Console-slim/dp/B0CY5HVDS2/?th=1",
    "thinkpad": "https://www.amazon.in/Lenovo-ThinkPad-Laptop-Windows-21JKS13L00/dp/B0D66YKRTZ/?th=1",
    "camera": "https://www.amazon.in/Sony-ZV-1-Microphone-Vlogging-Creation/dp/B08JVPJXMT/?th=1",
    "iphone": "https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX1W1XY?th=1",
}

# random user agent:
ua = UserAgent()
user_agent  = ua.random
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--user-agent={user_agent}')
# chrome_options.add_argument('--headless') # uncomment this line to run headless

def valid_page_format(driver, link):
    '''
    function to validate page format
    '''
    sleep(randint(4, 9))
    driver.get(link)
    sleep(randint(4, 9))
    try:
        review_section = driver.find_element(By.CLASS_NAME, 'review-views')
        if review_section:
            return driver
    except:
        return False

def scrape_data_and_save(amazon_link):
    '''
    function to scrape and save product
    data from amazon
    '''
    customer_reviews = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)
    right_format = valid_page_format(driver, amazon_link)
    while not right_format:
        driver.quit()
        print("trying again.. Invalid page Format found")
        sleep(randint(4, 7))
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)
        right_format = valid_page_format(driver, amazon_link)
    
    title = driver.find_element(By.CLASS_NAME, 'product-title-word-break').text
    try:
        price = driver.find_element(By.CLASS_NAME, 'priceToPay').text
        try:
            discount = driver.find_element(By.CLASS_NAME, 'savingsPercentage').text
        except:
            discount = "None"
    except:
        price = "Currently Unavailable"
        discount = "None"
    
    review_section = right_format.find_element(By.CLASS_NAME, 'review-views')
    if review_section:
        reviews = review_section.find_elements(By.CLASS_NAME, 'aok-relative')
        for review in reviews:
            date = review.find_element(By.CLASS_NAME, 'review-date').text.split('on ')[1].strip()
            review_title = review.find_element(By.CLASS_NAME, 'review-title').text
            rating = review.find_element(By.CLASS_NAME, 'a-icon-alt').get_attribute('textContent')
            text = review.find_element(By.CLASS_NAME, 'reviewText').text

            customer_reviews.append({
                'date': date,
                'title': review_title,
                'rating': rating,
                'text': text
            })

    driver.quit()
    return title, price, discount, customer_reviews

if __name__ == "__main__":
    date, time = datetime.now().strftime("%Y-%m-%d %H:%M").split(" ")
    hour, minute = time.split(":")
    last_scraped_data = []

    with open("assets/scraped_data_products.json", "r") as f:
        scraped_data = json.load(f)

    for key in tqdm(PRODUCTS_LINKS_MAP.keys(), desc="Scraping"):
        title, price, discount, customer_reviews = scrape_data_and_save(PRODUCTS_LINKS_MAP[key])

        # price data updation:
        price_data = [date, hour, minute, float(price.replace("₹", "").replace(",", ""))]
        with open(f"assets/price_history_data/{key}.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(price_data)

        # scraped data updation:
        sentiment = analyse_sentiment(customer_reviews)
        scraped_data.insert(0, {
            "date": date,
            "time": time,
            "title": title,
            "price": price,
            "discount": discount,
            "sentiment": sentiment,
            "reviews": customer_reviews
        })

        last_scraped_data.append({
            "date": date,
            "time": time,
            "title": title,
            "price": price,
            "discount": discount,
            "sentiment": sentiment
        })

        with open("assets/scraped_data_products.json", "w") as f:
            json.dump(scraped_data, f, indent=4, ensure_ascii=False)

    with open("assets/last_scraped_data.json", "w") as f:
        json.dump(last_scraped_data, f, indent=4, ensure_ascii=False)
