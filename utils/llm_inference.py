'''
function for sentiment analysis
using Google Gemini API
'''

import os
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

def provide_predictive_strategy(forecasted_prices, competitor_strategy):
    '''
    function to generate the analysis of
    competitor strategy based on
    scraped data of prices discounts
    and current date
    '''
    system_prompt = """Based on the Forecasted Prices of the given Products and the Competitor Strategy Analysis, provide a predictive strategy for the next 7 days. Make sure the response should be in 130-160 words only. Keep the dates in mind as well, and provide a detailed strategy based on the forecasted prices and competitor strategy. Here is the forecasted prices and competitor strategy:"""

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"{system_prompt}: \n{forecasted_prices}\n\n{competitor_strategy}")
    return response.text

def analyse_competitor_strategy(last_scraped_data: dict):
    '''
    function to generate the analysis of
    competitor strategy based on
    scraped data of prices discounts
    and current date
    '''
    system_prompt = """Analyse the competitor strategy based on the scraped data of prices, discounts and date. make sure the response should be in 130-160 words only. 
    observe the data given to you, and analyse it to infer strategical moves of the competitor for
    all the various products. mention the key points that you have observed. the date of the data
    is very important as well, keep in mind the Indian festival calender and infer information based
    on tha as well.

    Here is the last scraped data:"""
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"{system_prompt}: \n{last_scraped_data}")
    return response.text

def analyse_sentiment(product_reviews: list):
    '''
    function to analyse sentiment via using
    google gemini api
    '''
    system_prompt = """Analyse the sentiment of the following product reviews and provide the response in maximum of 20 words. # EXAMPLE OUTPUT: ['mostly positive, the customers are impressed by the product and have commended the service from the company']"""

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    review_catalogue = ""
    for i in range(len(product_reviews)):
        review = product_reviews[i]
        review_text = "\n".join(review.values())
        review_catalogue += review_text + "\n\n"

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"{system_prompt}: \n{review_catalogue}")
    return response.text
