import os
import json
from dotenv import load_dotenv # type: ignore
import requests

load_dotenv()
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

def format_notification(data):
    '''
    function to transform a python dictionary
    into the desired slack notification format
    '''
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
    '''
    function to send the slack notification
    '''
    payload = {"text": message}
    response = requests.post(slack_webhook, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
