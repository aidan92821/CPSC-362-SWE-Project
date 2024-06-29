import unittest
from unittest.mock import MagicMock
from DataAdapter import DataAdapter

class TestDataAdapter(unittest.TestCase):
    
    def test_notify(self):
        """Unit Test: Testing notify method"""
        data = {"Date": "2023-01-01", "Adj Close": 100}
        subscriber = MagicMock()
        
        adapter = DataAdapter()
        adapter.attach(subscriber)
        adapter.notify(data)
        
        subscriber.update.assert_called_once_with(data)
        print("[PASSED] notify method works as expected.")
        
if __name__ == '__main__':
    unittest.main()import unittest
from unittest.mock import MagicMock
from DataAdapter import DataAdapter

class TestDataAdapter(unittest.TestCase):
    
    def test_notify(self):
        """Unit Test: Testing notify method"""
        data = {"Date": "2023-01-01", "Adj Close": 100}
        subscriber = MagicMock()
        
        adapter = DataAdapter()
        adapter.attach(subscriber)
        adapter.notify(data)
        
        subscriber.update.assert_called_once_with(data)
        print("[PASSED] notify method works as expected.")
        
    def test_notify_without_subscriber(self):
        """Unit Test: Testing notify method without subscriber"""
        data = {"Date": "2023-01-01", "Adj Close": 100}
        
        adapter = DataAdapter()
        adapter.notify(data)
        
        # No assertion needed as there is no subscriber
        print("[PASSED] notify method without subscriber.")
        
    def test_notify_multiple_subscribers(self):
        """Unit Test: Testing notify method with multiple subscribers"""
        data = {"Date": "2023-01-01", "Adj Close": 100}
        subscriber1 = MagicMock()
        subscriber2 = MagicMock()
        
        adapter = DataAdapter()
        adapter.attach(subscriber1)
        adapter.attach(subscriber2)
        adapter.notify(data)
        
        subscriber1.update.assert_called_once_with(data)
        subscriber2.update.assert_called_once_with(data)
        print("[PASSED] notify method with multiple subscribers.")
        
if __name__ == '__main__':
    unittest.main()