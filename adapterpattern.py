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