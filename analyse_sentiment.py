'''
function for sentiment analysis
using Google Gemini API
'''

import google.generativeai as genai # type: ignore
from utils import system_prompt

def analyse_sentiment(product_reviews: list):
    '''
    function to analyse sentiment via using
    google gemini api
    '''
    genai.configure(api_key="AIzaSyCBmhM80jMMm1XJINUQZNDfSMqZiS6fuGE")
    review_catalogue = ""
    for i in range(len(product_reviews)):
        review = product_reviews[i]
        review_text = "\n".join(review.values())
        review_catalogue += review_text + "\n\n"

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"{system_prompt}: \n{review_catalogue}")
    return response.text
