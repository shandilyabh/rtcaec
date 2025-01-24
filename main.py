'''
streamlit UI for the app
'''

import streamlit as st  # type: ignore
from utils.arima import forecast_product_prices
import subprocess
import pandas as pd
import json
import time
from datetime import datetime
from utils.slack_notification import send_to_slack

def load_data():
    with open("assets/last_scraped_data.json", "r") as f:
        return json.load(f)

def scrape():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.write("Running the scraping script...")
    result = subprocess.run(['python', 'scrape.py'], capture_output=True, text=True)

    if result.returncode == 0:
        st.success("Scraping script executed successfully!")
        send_to_slack(f"Manual Scraping was successful. {now}")
        st.text(result.stdout)
        
        st.session_state['data'] = load_data()
        st.experimental_rerun()

    else:
        st.error("Error while running the script.")
        st.text(result.stderr) 

if 'data' not in st.session_state:
    st.session_state['data'] = load_data()

df = pd.DataFrame(st.session_state['data'])
df.columns = ['Date', 'Time', 'Title', 'Price', 'Discount', 'Sentiment']

st.title('Real-Time Competitor Analysis for E-Commerce')

st.write("Last Scraped Data:")
st.table(df)

scrape_button = st.button('Scrape Product Data')

if scrape_button:
    scrape()

model = st.selectbox('Select Model:', ['Sony Digital Camera', 'Lenovo Thinkpad E14', 'Samsung Galaxy S23 Ultra', 'Apple iPhone 15', 'Whirpool Washing Machine', 'Sony Playstation 5 Console'])
num_days = st.number_input('Number of Days:', min_value=1, max_value=365, step=1)
forecast_button = st.button('Start Forecasting')

if forecast_button:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if model == "Sony Digital Camera":
        model_name = "assets/forecasting_assets/models/camera_arima_model.joblib"
    elif model == "Lenovo Thinkpad E14":
        model_name = "assets/forecasting_assets/models/thinkpad_arima_model.joblib"
    elif model == "Samsung Galaxy S23 Ultra":
        model_name = "assets/forecasting_assets/models/s23_arima_model.joblib"
    elif model == "Apple iPhone 15":
        model_name = "assets/forecasting_assets/models/iphone_arima_model.joblib"
    elif model == "Whirpool Washing Machine":
        model_name = "assets/forecasting_assets/models/whirpool_arima_model.joblib"
    elif model == "Sony Playstation 5 Console":
        model_name = "assets/forecasting_assets/models/ps5_arima_model.joblib"
    
    results = forecast_product_prices(model_name, num_days)
    forecast_df = pd.DataFrame({
        'Day': [f"Day {i+1}" for i in range(num_days)],
        'Forecasted Value': results
    })
    time.sleep(3)
    st.table(forecast_df)
    send_to_slack(f"Forecast were generated successfully for {model}. {now}")