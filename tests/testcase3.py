import unittest
from PyQt5.QtWidgets import QApplication
from download_data_gui import DownloadDataGUI, DataSourceAdapter
from unittest.mock import MagicMock
from Model.download_data import download_stock_data, save_to_json

class TestDownloadDataGUI(unittest.TestCase):
    
    def setUp(self):
        # Initialize DownloadDataGUI with mock DataSourceAdapter
        self.app = QApplication([])
        self.adapter = DataSourceAdapter(download_stock_data, save_to_json)
        self.gui = DownloadDataGUI(self.adapter)
    
    def test_download_data_button_click(self):
        # Test user interaction with download button
        self.gui.symbol_input.setText('SOXL')
        self.gui.start_date.setSelectedDate(self.gui.start_date.minimumDate())
        self.gui.end_date.setSelectedDate(self.gui.end_date.maximumDate())
        # Simulate button click event
        self.gui.download_data()
        # Assert success message or other expected behavior
        # Add more assertions as needed
    
    # Add more test cases for other functionalities in DownloadDataGUI
    
if __name__ == '__main__':
    unittest.main()
