import yfinance as yf
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Function to fetch data
def fetch_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data

# Function to save data to a JSON file
def save_to_json(data, filename):
    # Convert keys to string for JSON serialization
    data_str_keys = {str(key): value for key, value in data.items()}
    with open(filename, 'w') as f:
        json.dump(data_str_keys, f)

# Function to load data from a JSON file
def load_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    # Convert keys back to datetime for further processing
    data_dt_keys = {datetime.strptime(key, '%Y-%m-%d %H:%M:%S'): value for key, value in data.items()}
    return data_dt_keys

# Function to plot data
def plot_data(data, title):
    plt.figure(figsize=(12, 6))
    for ticker, df in data.items():
        dates = list(df.keys())
        closes = [value['Close'] for value in df.values()]
        plt.plot(dates, closes, label=ticker)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.show()

# Specify the date range
start_date = '2023-01-01'
end_date = '2023-12-31'

# Fetch data for SOXL and SOXS
soxl_data = fetch_data('SOXL', start_date, end_date)
soxs_data = fetch_data('SOXS', start_date, end_date)

# Convert data to dictionary format for JSON serialization
soxl_data_dict = soxl_data.to_dict('index')
soxs_data_dict = soxs_data.to_dict('index')

# Save data to JSON files
save_to_json({'SOXL': soxl_data_dict}, 'soxl_data.json')
save_to_json({'SOXS': soxs_data_dict}, 'soxs_data.json')

# Load data from JSON files
loaded_soxl_data = load_from_json('soxl_data.json')
loaded_soxs_data = load_from_json('soxs_data.json')

# Combine loaded data
combined_data = {
    'SOXL': loaded_soxl_data,
    'SOXS': loaded_soxs_data
}

# Plot the data
plot_data(combined_data, 'SOXL and SOXS ETF Prices')