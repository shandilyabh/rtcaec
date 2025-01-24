
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

### Procedure to Retrieve a Slack Incoming Webhook URL:

1. **Log in to Slack**: Open your Slack workspace in a browser or the app.
2. **Go to API Website**: Navigate to [Slack API](https://api.slack.com/).
3. **Create an App**:
   - Click on **"Create an App"**.
   - Choose **"From scratch"** and name your app.
   - Select the workspace where the app will be used.
4. **Enable Incoming Webhooks**:
   - In your app settings, go to **"Incoming Webhooks"**.
   - Toggle **"Activate Incoming Webhooks"** to ON.
5. **Add a Webhook to a Channel**:
   - Scroll down and click **"Add New Webhook to Workspace"**.
   - Select the channel where messages will be sent.
   - Click **"Allow"**.
6. **Copy Webhook URL**:
   - After adding, the webhook URL will be displayed.
   - Copy and use it in your application.

### 2. Retrieve Gemini API Key
- Obtain a Gemini API key.
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

- `llm_inference.py`: functions using Gemini API for sentiment analysis and strategy prediction and suggestion.
- `arima.py`: Functions for training ARIMA models and forecasting prices.
- `slack_notification.py`: Functions for sending notifications via Slack.

---

## Daily Task Workflow

This project has a daily task for scraping product data. It is managed via GitHub Actions in the file `.github/workflows/daily_scrape.yml`.
