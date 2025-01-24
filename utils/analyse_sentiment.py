'''
function for sentiment analysis
using Google Gemini API
'''

import os
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

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
