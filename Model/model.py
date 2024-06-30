import json
import os

class DataSourceInterface:
    def get_data(self, ticker):
        raise NotImplementedError("This method should be overridden.")

class JSONDataSource(DataSourceInterface):
    def __init__(self, base_path):
        self.base_path = base_path

    def get_data(self, ticker):
        file_path = os.path.join(self.base_path, f"{ticker}_data.json")
        if not os.path.exists(file_path):
            print(f"File not found for ticker: {ticker}")
            return None
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

class Publisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify(self, data):
        for subscriber in self.subscribers:
            subscriber.update(data)
