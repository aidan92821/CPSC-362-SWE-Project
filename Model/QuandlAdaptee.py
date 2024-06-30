import quandl
import json

class QuandlDataSource:
    def __init__(self):
        self.api_key = 'YOUR_API_KEY'
        quandl.ApiConfig.api_key = self.api_key

    def get_data(self, ticker, start_date=None, end_date=None):
        data = quandl.get(ticker, start_date=start_date, end_date=end_date)
        return data.reset_index().to_dict(orient='records')

    def save_to_json(self, ticker, start_date, end_date, file_name):
        data = self.get_data(ticker, start_date, end_date)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {file_name}")
