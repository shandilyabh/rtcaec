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
from utils.llm_inference import (
    analyse_competitor_strategy as anls,
    provide_predictive_strategy as pps   
)
from utils.slack_notification import send_to_slack

# Function to load data
def load_data():
    with open("assets/last_scraped_data.json", "r") as f:
        return json.load(f)

# Function to run the scraping
def scrape():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.write("Running the scraping script...")
    result = subprocess.run(['python', 'scrape.py'], capture_output=True, text=True)

    if result.returncode == 0:
        st.success("Scraping script executed successfully!")
        send_to_slack(f"Manual Scraping was successful. {now}")
        st.text(result.stdout)
        
        # Load new scraped data and update session state
        st.session_state['data'] = load_data()
        st.experimental_rerun()  # Refresh the page to update content

    else:
        st.error("Error while running the script.")
        st.text(result.stderr) 

# Default session state data
if 'data' not in st.session_state:
    st.session_state['data'] = load_data()

competitor_strategy = anls(load_data())

df = pd.DataFrame(st.session_state['data'])
df.columns = ['Date', 'Time', 'Title', 'Price', 'Discount', 'Sentiment']

# Title of the project
st.title('Real-Time Competitor Analysis for E-Commerce')

# Sidebar with options
st.sidebar.title('Navigation')

# Default option is empty to show instructions first
option = st.sidebar.radio('Select Option', ['Main Page', 'Competitor Strategy', 'Product Data', 'Forecast & Strategy'])

# Default screen when no option is chosen
if option == 'Main Page':
    st.image("assets/rtcaec.png")
    st.write("### Instructions:")
    st.write("""
    - **Competitor Strategy**: Displays the analysis of competitors' strategies based on the last scraped data.
    - **Product Data**: Displays the last scraped product data and allows for manual scraping. This will also show the updated competitor strategy after a successful scrape.
    - **Forecast Product Prices**: Select a product model and forecast its prices for a set number of days. It will show the forecast and a suggested strategy.
    """)
    
elif option == 'Competitor Strategy':
    st.write("### Competitor Strategy Analysis:")
    # competitor_strategy = anls(load_data())
    st.write(competitor_strategy)

elif option == 'Product Data':
    # Display Product Data and Scraping Options
    st.write("#### Last Scraped Data:")
    st.table(df)
    
    st.write("**Competitor Strategy Analysis:**")
    # competitor_strategy = anls(load_data())
    st.write(competitor_strategy)

    # Manual Scrape Button
    st.markdown("<h2 style='font-size:24px;'>Initiate Manual Scraping:</h2>", unsafe_allow_html=True)
    scrape_button = st.button('Scrape Product Data')

    if scrape_button:
        scrape()

elif option == 'Forecast & Strategy':
    # Forecasting Section
    # competitor_strategy = anls(load_data())
    st.markdown("<h2 style='font-size:24px;'>Forecasting and Strategy:</h2>", unsafe_allow_html=True)

    model = st.selectbox('Select Model:', ['Sony Digital Camera', 'Lenovo Thinkpad E14', 'Samsung Galaxy S23 Ultra', 'Apple iPhone 15', 'Whirpool Washing Machine', 'Sony Playstation 5 Console'])
    num_days = st.number_input('Number of Days:', min_value=1, max_value=365, step=1)
    forecast_button = st.button('Forecast')

    if forecast_button:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Set model path based on selected product
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

        st.table(forecast_df)
        send_to_slack(f"Forecasted Prices were generated successfully for {model}. {now}")

        st.write("**Suggested Strategy based on Price Forcasting & Competitor Analysis:**")
        st.write(pps(results, competitor_strategy))