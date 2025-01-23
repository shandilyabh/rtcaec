'''
script for terminal interface and slack notification
'''

from analyse_sentiment import analyse_sentiment
from scrape import scrape_review_data_and_save, scrape_realtime_price_data
from utils import products_links_map, send_to_slack, format_notification
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from pyfiglet import Figlet # type: ignore

def rcanalysis():
    os.system("clear")
    figlet = Figlet(font='standard')
    print(figlet.renderText('Real Time Competitor Analysis'))
    print("\n")

def predict_future_prices(product_name, file_path, x_days):
    '''
    function to forecast price
    '''
    df = pd.read_csv(file_path)
    
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date', inplace=True)

    df_product = df[df['product'] == product_name]
    if df_product.empty:
        return f"No data available for product: {product_name}"

    X = df_product['date'].astype(int).values.reshape(-1, 1)
    y = df_product['price'].values

    model = LinearRegression()
    model.fit(X, y)

    last_date = df_product['date'].max()
    future_dates = pd.date_range(last_date, periods=x_days + 1, freq='D')[1:]
    future_X = future_dates.astype(int).values.reshape(-1, 1)
    future_prices = model.predict(future_X)

    # Output predictions
    predictions = pd.DataFrame({'Date': future_dates, 'Predicted Price': future_prices})
    return predictions

def process_and_present(product, forecast_for_days):
    price_data = scrape_realtime_price_data(products_links_map[product])
    review_data = scrape_review_data_and_save({product: products_links_map[product]})
    sentiment_data = analyse_sentiment(review_data[product])
    
    print("\n")
    for key in price_data.keys():
        print(f"{key}: {price_data.get(key)}")
    
    print(sentiment_data)
    
    file_path = 'data.csv'
    predictions = predict_future_prices(product, file_path, forecast_for_days)
    print(predictions)
    print("\n")

    data = {
        "Product": price_data['title'],
        "Price" : price_data['price'],
        "Discount": price_data['discount on MRP'],
        "Customer Sentiment": sentiment_data,
        "forecast": predictions
    }
    message = format_notification(data)

    # Sending message to Slack
    send_to_slack(message)
    print(f"Sent notification:\n{message}")

def main():
    rcanalysis()
    products = {
        1: "iphone 15",
        2: "lenovo thinkpad",
        3: "sony minvlogging camera",
        4: "samsung s23",
        5: "playstation 5"
    }

    print("Choose from the products below (ENTER THE CORRESPONDING NUMBER, eg. 1):")
    print("1. Apple iPhone 15\n2. Lenovo Thinkpad Laptop\n3. Sony Minivlogging Camera\n4. Samsung Galaxy S23\n5. SOny Playstation 5")
    index = int(input("\nEnter the Number: ").strip())
    print("You have selected: ", products[index])
    forecast_for_days = int(input("Enter the number of days you want to forecast for: ").strip())
    print("\n")

    process_and_present(products[index], forecast_for_days)

if __name__ == "__main__":
    main()