import yfinance as yf
import pandas as pd
import json

def download_stock_data(symbol, start_date, end_date):
    """
    Download historical stock data from Yahoo Finance.

    Parameters:
    symbol (str): The ticker symbol of the stock.
    start_date (str): The start date for downloading data in 'YYYY-MM-DD' format.
    end_date (str): The end date for downloading data in 'YYYY-MM-DD' format.

    Returns:
    DataFrame: A Pandas DataFrame containing the historical stock data.
    """
    data = yf.download(symbol, start=start_date, end=end_date)
    print(f"Downloaded data for {symbol}:")
    print(data.head())  # Print first few rows of the data for verification
    return data

def save_to_json(data, filename):
    """
    Save the stock data to a JSON file.

    Parameters:
    data (DataFrame): The Pandas DataFrame containing the stock data.
    filename (str): The name of the file to save the data to.
    """
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].astype(str)  # Convert the Date column to string
    data_dict = data.to_dict(orient='records')
    with open(filename, 'w') as f:
        json.dump(data_dict, f, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Define the list of stock symbols to download
    symbols = ["SOXL", "SOXS"]
    # Define the start and end dates for the data download
    start_date = "2021-01-01"
    # Get today's date in 'YYYY-MM-DD' format
    end_date = pd.to_datetime("today").strftime('%Y-%m-%d')

    # Loop through each symbol and download its data
    for symbol in symbols:
        print(f"Downloading data for {symbol}")
        data = download_stock_data(symbol, start_date, end_date)
        if data.empty:
            print(f"No data downloaded for {symbol}.")
        else:
            # Define the filename for saving the data
            filename = f"{symbol}_data.json"
            print(f"Saving data to {filename}")
            save_to_json(data, filename)
            print(f"Data saved to {filename}")
