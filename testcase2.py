import unittest
from unittest.mock import MagicMock
from datetime import datetime
from download_data_gui import DataSourceAdapter, Publisher
from GUI import CalendarPlotApp 

class TestPublisherSubscriber(unittest.TestCase):
    def setUp(self):
        # Create mock functions for testing
        self.mock_download_function = MagicMock()
        self.mock_save_function = MagicMock()

        # Create instances of DataSourceAdapter and DataPublisher
        self.data_source = DataSourceAdapter(self.mock_download_function, self.mock_save_function)
        self.publisher = Publisher()

        # Pass data_source and publisher to CalendarPlotApp
        self.calendar_app = CalendarPlotApp(self.data_source, self.publisher)

    def test_data_updated_event(self):
        # Simulate data update event
        new_data = {"date": "2024-06-30", "value": 100.0}
        
        # Mock download function behavior
        self.mock_download_function.return_value = new_data
        
        # Trigger data update in the DataSourceAdapter
        self.data_source.download_data('SOXL', '2024-06-30', '2024-06-30')

        # Verify that CalendarPlotApp has updated its data
        updated_data = self.calendar_app.get_updated_data()  # Implement this method in CalendarPlotApp
        expected_data = {"date": "2024-06-30", "value": 100.0}
        
        self.assertEqual(updated_data, expected_data, "CalendarPlotApp did not receive expected updated data.")

if __name__ == '__main__':
    unittest.main()
