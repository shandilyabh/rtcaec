
# Real Time Competitor Analysis for E-Commerce

This project tracks Amazon product prices, forecasts future prices using ARIMA models, and sends notifications via Slack.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Setup

### 1. Retrieve Slack Incoming Webhook URL
- Create a Slack app and configure an **incoming webhook** for a Slack channel.
- Note down the Webhook URL.

### 2. Retrieve Gemini API Key
- Obtain a Gemini API key for sentiment analysis.
- Keep the key securely stored for configuration.

---

## Running the Application

1. After setting up the Slack Incoming Webhook URL and Gemini API key, run the app with Streamlit:
   ```bash
   streamlit run main.py
   ```

---

## Project Structure

- `scrape.py`: Scrapes data from Amazon using product links from `PRODUCTS_LINKS_MAP`.
- `assets/scraped_data_products.json`: Stores the accumulated scraped data.
- `assets/last_scraped_data`: Contains data from the latest scraping run.
- `assets/forecasting_assets/models`: ARIMA models for price forecasting.
- `assets/forecasting_assets/arima_training_data`: Training data for ARIMA models.
- `assets/price_history_data`: Daily price records in CSV format.

---

## Helper Functions in `utils/`

- `analyse_sentiment.py`: Sentiment analysis using Gemini API.
- `arima.py`: Functions for training ARIMA models and forecasting prices.
- `slack_notification.py`: Functions for sending notifications via Slack.

---

## Daily Task Workflow

This project has a daily task for scraping product data. It is managed via GitHub Actions in the file `.github/workflows/daily_scrape.yml`.
