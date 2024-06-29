import unittest
import pandas as pd
from simpleMovingAverage import parse_data, calculate_sma, backtest, run_sma_and_backtest
import json

class TestTradingSystem(unittest.TestCase):
    
    def setUp(self):
        # Sample data for testing
        self.data = [
            {"Date": "2023-01-01", "Adj Close": 100},
            {"Date": "2023-01-02", "Adj Close": 105},
            {"Date": "2023-01-03", "Adj Close": 110},
            {"Date": "2023-01-04", "Adj Close": 115},
            {"Date": "2023-01-05", "Adj Close": 120}
        ]
        self.df = parse_data(self.data)
        
    def test_parse_data(self):
        """Unit Test: Testing parse_data function"""
        print("\nUnit Test: Testing parse_data function")
        self.assertEqual(len(self.df), 5)
        self.assertEqual(self.df.index[0], pd.Timestamp('2023-01-01'))
        print("[PASSED] parse_data function works as expected.")
        
    def test_calculate_sma(self):
        """Unit Test: Testing calculate_sma function"""
        print("\nUnit Test: Testing calculate_sma function")
        df_sma = calculate_sma(self.df, short_window=2, long_window=3)
        self.assertIn('STA', df_sma.columns)
        self.assertIn('LTA', df_sma.columns)
        print("[PASSED] calculate_sma function works as expected.")
        
    def test_backtest(self):
        """Integration Test: Testing backtest function with sample data"""
        print("\nIntegration Test: Testing backtest function with sample data")
        df_sma = calculate_sma(self.df, short_window=2, long_window=3)
        log, log_data = backtest(df_sma, stock='SOXL')
        self.assertGreater(len(log), 0)
        self.assertGreater(len(log_data), 0)
        print("[PASSED] backtest function works as expected.")
        
    def test_run_sma_and_backtest(self):
        """Integration Test: Testing run_sma_and_backtest function"""
        print("\nIntegration Test: Testing run_sma_and_backtest function")
        with open('test_data.json', 'w') as f:
            json.dump(self.data, f)
        log_file, csv_file = run_sma_and_backtest('test_data.json', 'SOXL')
        self.assertTrue(log_file.endswith('.txt'))
        self.assertTrue(csv_file.endswith('.csv'))
        print("[PASSED] run_sma_and_backtest function works as expected.")
        
if __name__ == '__main__':
    unittest.main()
