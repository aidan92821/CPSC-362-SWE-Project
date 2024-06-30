import yfinance as yf
import json
import pandas as pd

class YFinanceDataSource:
    def get_data(self, ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        return data.reset_index().to_dict(orient='records')

    def save_to_json(self, ticker, start_date, end_date, file_name):
        data = self.get_data(ticker, start_date, end_date)
        for item in data:
            if isinstance(item['Date'], pd.Timestamp):
                item['Date'] = item['Date'].strftime('%Y-%m-%d')
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {file_name}")
