import unittest
from download_data_gui import DataSourceAdapter
from Model.download_data import download_stock_data, save_to_json

class TestDataSourceAdapter(unittest.TestCase):
    
    def setUp(self):
        # Initialize DataSourceAdapter with mock download functions
        self.adapter = DataSourceAdapter(download_stock_data, save_to_json)
    
    def test_download_data(self):
        # Test downloading data using the adapter
        symbol = 'SOXL'
        start_date = '2023-01-01'
        end_date = '2023-06-30'
        data = self.adapter.download_data(symbol, start_date, end_date)
        self.assertIsNotNone(data)
        # Add more assertions as needed
    
    
if __name__ == '__main__':
    unittest.main()
