
# Real-Time Competitor Analysis for E-Commerce

This project retrieves product data, analyzes sentiment, and forecasts prices, then sends an update to a Slack channel using a webhook.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate into the project directory:
   ```bash
   cd <project-directory>
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Retrieving Slack Incoming Webhook

1. Go to your Slack workspace.
2. Navigate to **Apps** > **Incoming Webhooks**.
3. Create a new webhook and copy the URL provided.

## Retrieving Gemini API Key

1. Visit the Gemini API documentation or developer portal.
2. Sign in and generate an API key for accessing product data.
3. Save the API key securely for use in this project.

## Running the Script

1. Open a terminal.
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```
3. Run the script:
   ```bash
   python interface.py
   ```

## Example Slack Message

When the script is executed, the following type of message will be sent to the configured Slack channel via the webhook:

```
Title: Sony Digital Camera ZV-1 Only (Compact, Video Eye AF, Flip Screen, in-Built Microphone, 4K Vlogging Camera for Content Creation) - Black  
Price: ₹49,990  
Discount: -26%  
Sentiment: Mostly positive; praised for video quality and autofocus, but criticized for battery life and price.

----
Forecast:
----
    1    2024-10-10 00:00:00    53188.248714135814  
    2    2024-10-11 00:00:00    53200.97912943474  
    3    2024-10-12 00:00:00    53213.70954473366  
    4    2024-10-13 00:00:00    53226.439960032614  
```

## Notes

- Ensure the Slack webhook URL and Gemini API key are correctly configured in the script before running.
- Modify the `interface.py` script as necessary to suit your specific needs.
