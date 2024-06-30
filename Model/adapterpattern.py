from Model.QuandlAdaptee import QuandlDataSource
from Model.YFinanceAdaptee import YFinanceDataSource

class DataSourceAdapter:
    def __init__(self):
        self.quandl_source = QuandlDataSource()
        self.yfinance_source = YFinanceDataSource()

    def download_data(self, ticker, start_date, end_date, file_name):
        if 'BCHARTS' in ticker:
            self.quandl_source.save_to_json(ticker, start_date, end_date, file_name)
        else:
            self.yfinance_source.save_to_json(ticker, start_date, end_date, file_name)
