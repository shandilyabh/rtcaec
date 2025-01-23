"""
Scrape Products data from Amazon
"""

from selenium import webdriver # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from time import sleep
from fake_useragent import UserAgent # type: ignore
import json
from random import randint
from tqdm import tqdm

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

def scrape_data_and_save(products_links_map):
    '''
    function to scrape and save product
    data from amazon
    '''
    review_data = {}
    for product in tqdm(products_links_map.keys(), desc="Scraping Product Data"):
        customer_reviews = []
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)
        right_format = valid_page_format(driver, products_links_map[product])
        while not right_format:
            driver.quit()
            print("trying again.. Invalid page Format found")
            sleep(randint(4, 7))
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)
            right_format = valid_page_format(driver, products_links_map[product])
        
        title = driver.find_element(By.CLASS_NAME, 'product-title-word-break').text
        price = driver.find_element(By.CLASS_NAME, 'priceToPay').text
        try:
            discount = driver.find_element(By.CLASS_NAME, 'savingsPercentage').text
        except:
            discount = "not specified on the site"
        
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
        review_data[product] = customer_reviews
        with open("customer_reviews_test.json", "w") as file:
            json.dump(review_data, file, indent=4)
        del customer_reviews
        driver.quit()
    
    del products_links_map

    return title, price, discount, review_data
