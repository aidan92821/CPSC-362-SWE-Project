import json

class DataSourceInterface:
    def get_data(self, ticker):
        raise NotImplementedError("This method should be overridden.")

class JSONDataSource(DataSourceInterface):
    def __init__(self, file_path):
        self.file_path = file_path

    def get_data(self, ticker):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data.get(ticker, None)

class Publisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def notify(self, data):
        for subscriber in self.subscribers:
            subscriber.update(data)
