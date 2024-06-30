import yfinance as yf
import pandas as pd
import json
from datetime import datetime

class DataSourceType:
    Yahoo = 'Yahoo'
    Local = 'Local'

class HistoricalData_Adapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def get_historical_data(self):
        return self.adaptee.get_historical_data()

class Yahoo_HistoricalData:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol.upper()
        self.start_date = start_date
        self.end_date = end_date

    def get_historical_data(self):
        ticker = yf.Ticker(self.symbol)
        if 'symbol' not in ticker.info:
            raise ValueError(f"{self.symbol} is invalid, no data found.")
        df = ticker.history(start=self.start_date, end=self.end_date)
        return df

class Local_HistoricalData:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol.upper()
        self.start_date = start_date
        self.end_date = end_date

    def get_historical_data(self):
        # For the purpose of this example, we'll read from a JSON file
        try:
            with open(f'{self.symbol}_data.json', 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            # Filter the dataframe based on the date range
            df['Date'] = pd.to_datetime(df['Date'])
            mask = (df['Date'] >= self.start_date) & (df['Date'] <= self.end_date)
            return df.loc[mask]
        except FileNotFoundError:
            raise ValueError(f"No local historical data found for {self.symbol}.")

def get_historical_data(symbol, start_date, end_date, data_source=DataSourceType.Yahoo):
    symbol = symbol.upper()
    
    if data_source == DataSourceType.Local:
        adaptee = Local_HistoricalData(symbol, start_date, end_date)
    elif data_source == DataSourceType.Yahoo:
        adaptee = Yahoo_HistoricalData(symbol, start_date, end_date)
    else:
        raise ValueError(f"Unsupported data source: {data_source}")

    data_adapter = HistoricalData_Adapter(adaptee)
    return data_adapter.get_historical_data()


