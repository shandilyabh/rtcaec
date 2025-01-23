import os
import json
from dotenv import load_dotenv # type: ignore
import requests

load_dotenv()
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

system_prompt = """Analyse the sentiment of the following product reviews and provide the response in maximum of 20 words.

# EXAMPLE OUTPUT: ['mostly positive, the customers are impressed by the product and have commended the service from the company']
"""

products_links_map = {
    "samsung s23": "https://www.amazon.in/Samsung-Galaxy-Ultra-Phantom-Storage/dp/B0BT9FDZ8N/?th=1",
    "whirpool washing machine": "https://www.amazon.in/Whirlpool-Fully-Automatic-WHITEMAGIC-ROYAL-7-0/dp/B08QP41KBP/?th=1",
    "playstation 5": "https://www.amazon.in/Sony-CFI-2008A01X-PlayStation%C2%AE5-Console-slim/dp/B0CY5HVDS2/?th=1",
    "lenovo thinkpad": "https://www.amazon.in/Lenovo-ThinkPad-Laptop-Windows-21JKS13L00/dp/B0D66YKRTZ/?th=1",
    "sony minvlogging camera": "https://www.amazon.in/Sony-ZV-1-Microphone-Vlogging-Creation/dp/B08JVPJXMT/?th=1",
    "iphone 15": "https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX1W1XY?th=1"
}

def format_notification(data):
    forecast_df = data["forecast"]
    forecast = "\n".join(
        [f"\t{index + 1}\t{row['Date']}\t{row['Predicted Price']}" for index, row in forecast_df.iterrows()]
    )
    return (
        f"title: {data['Product']}\n"
        f"price: {data['Price']}\n"
        f"discount: {data['Discount']}\n"
        f"sentiment: {data['Customer Sentiment']}\n"
        f"----\nForecast:\n----\n{forecast}"
    )

def send_to_slack(message):
    payload = {"text": message}
    response = requests.post(slack_webhook, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
