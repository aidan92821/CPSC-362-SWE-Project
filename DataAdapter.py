import os
import json
from datetime import datetime

class DataAdapter:
    def get_ticker_list(self):
        return [f.split('_')[0] for f in os.listdir() if f.endswith('_data.json')]

    def fetch_data(self, ticker, start_date=None, end_date=None):
        if isinstance(start_date, datetime):
            start_date = start_date.strftime('%Y-%m-%d')
        if isinstance(end_date, datetime):
            end_date = end_date.strftime('%Y-%m-%d')

        file_name = f"{ticker}_data.json"
        with open(file_name, 'r') as file:
            data = json.load(file)

        if isinstance(data, list):
            data = {entry['Date'].split()[0]: entry for entry in data}  # Split on space to remove time

        filtered_data = {
            datetime.strptime(date, '%Y-%m-%d').date(): info
            for date, info in data.items()
            if (start_date is None or date >= start_date) and (end_date is None or date <= end_date)
        }

        return filtered_data
