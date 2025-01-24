'''
Functions used for - 

:train an ARIMA model using a csv file containing price history
:do forecasting using the trained ARIMA model

train_arima_model('ps5.csv', 'ps5_arima_model.joblib')

'''

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA # type: ignore
import joblib

def train_arima_model(csv_file_path, model_save_path):
    df = pd.read_csv(csv_file_path)
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Hour'].astype(str) + ':' + df['Minute'].astype(str))
    df.set_index('Datetime', inplace=True)
    df.sort_index(inplace=True)
    price_data = df['Price']
    
    model = ARIMA(price_data, order=(5, 1, 0))
    model_fit = model.fit()
    
    joblib.dump(model_fit, model_save_path)
    
    print(f"ARIMA model saved at: {model_save_path}")

def forecast_product_prices(model_path, x_days):
    model_fit = joblib.load(model_path)
    forecast = model_fit.forecast(steps=x_days)
    return forecast