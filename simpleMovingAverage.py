import pandas as pd
import json

# Function to parse data from JSON
def parse_data(data):
    """
    Parse the JSON data into a Pandas DataFrame.

    Parameters:
    data (dict): The data loaded from a JSON file.

    Returns:
    df (DataFrame): The parsed data as a DataFrame with the date as the index.
    """
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

# Function to calculate SMA
def calculate_sma(df, short_window=20, long_window=100):
    """
    Calculate the Simple Moving Averages (STA and LTA) for the given DataFrame.

    Parameters:
    df (DataFrame): The DataFrame containing stock data.
    short_window (int): The window size for the short-term moving average.
    long_window (int): The window size for the long-term moving average.

    Returns:
    df (DataFrame): The DataFrame with additional columns for STA and LTA.
    """
    df['STA'] = df['Adj Close'].rolling(window=short_window).mean()
    df['LTA'] = df['Adj Close'].rolling(window=long_window).mean()
    df.dropna(inplace=True)
    return df

# Function to perform backtest
def backtest(df, initial_balance=100000, stock='SOXL'):
    """
    Backtest the trading strategy using SMA.

    Parameters:
    df (DataFrame): The DataFrame containing stock data with STA and LTA columns.
    initial_balance (float): The initial balance for the backtest.
    stock (str): The stock symbol being backtested ('SOXL' or 'SOXS').

    Returns:
    log (list): A list of strings containing the backtest log.
    df_log (DataFrame): The DataFrame containing the log for CSV export.
    """
    balance = initial_balance
    shares = 0
    log = []

    # Log headers for the backtest results
    log.append(f"{'DATE':<12}{'buy/sell':<10}{'STA':<8}{'LTA':<8}{'balance':<15}{'amount of stock':<15}")
    log.append("-" * 70)
    
    log_data = []
    buy_sell_triggered = False

    # Iterate over each row in the DataFrame to apply the trading strategy
    for date, row in df.iterrows():
        date_str = date.strftime('%m-%d-%y')
        if stock == 'SOXL':
            if row['STA'] > row['LTA']:  # Buy signal for SOXL
                if balance > row['Adj Close']:
                    shares_to_buy = balance // row['Adj Close']
                    balance -= shares_to_buy * row['Adj Close']
                    shares += shares_to_buy
                    log.append(f"{date_str:<12}{'BUY':<10}{row['STA']:<8.2f}{row['LTA']:<8.2f}{balance:<15.2f}{shares:<15}")
                    log_data.append([date_str, 'BUY', row['STA'], row['LTA'], balance, shares])
                    buy_sell_triggered = True
            elif row['STA'] < row['LTA'] and shares > 0:  # Sell signal for SOXL
                balance += shares * row['Adj Close']
                log.append(f"{date_str:<12}{'SELL':<10}{row['STA']:<8.2f}{row['LTA']:<8.2f}{balance:<15.2f}{shares:<15}")
                log_data.append([date_str, 'SELL', row['STA'], row['LTA'], balance, shares])
                shares = 0
                buy_sell_triggered = True
        elif stock == 'SOXS':
            if row['STA'] < row['LTA']:  # Buy signal for SOXS
                if balance > row['Adj Close']:
                    shares_to_buy = balance // row['Adj Close']
                    balance -= shares_to_buy * row['Adj Close']
                    shares += shares_to_buy
                    log.append(f"{date_str:<12}{'BUY':<10}{row['STA']:<8.2f}{row['LTA']:<8.2f}{balance:<15.2f}{shares:<15}")
                    log_data.append([date_str, 'BUY', row['STA'], row['LTA'], balance, shares])
                    buy_sell_triggered = True
            elif row['STA'] > row['LTA'] and shares > 0:  # Sell signal for SOXS
                balance += shares * row['Adj Close']
                log.append(f"{date_str:<12}{'SELL':<10}{row['STA']:<8.2f}{row['LTA']:<8.2f}{balance:<15.2f}{shares:<15}")
                log_data.append([date_str, 'SELL', row['STA'], row['LTA'], balance, shares])
                shares = 0
                buy_sell_triggered = True

    # Final log entry for remaining balance if any shares are left
    if shares > 0:
        balance += shares * df.iloc[-1]['Adj Close']
        final_date_str = df.index[-1].strftime('%m-%d-%y')
        log.append("\n" + "-" * 70)
        log.append(f"{final_date_str:<12}{'FINAL SELL':<10}{df.iloc[-1]['STA']:<8.2f}{df.iloc[-1]['LTA']:<8.2f}{balance:<15.2f}{shares:<15}")
        log_data.append([final_date_str, 'FINAL SELL', df.iloc[-1]['STA'], df.iloc[-1]['LTA'], balance, shares])
        buy_sell_triggered = True

    # Add a message if no buy/sell signals were triggered
    if not buy_sell_triggered:
        log.append("\nNo buy or sell signals have been triggered between the dates selected.")
        log_data.append(["N/A", "N/A", "N/A", "N/A", balance, shares])

    df_log = pd.DataFrame(log_data, columns=["DATE", "buy/sell", "STA", "LTA", "balance", "amount of stock"])
    return log, df_log

# Function to run SMA and backtest
def run_sma_and_backtest(file_path, stock, start_date=None, end_date=None):
    """
    Load data from a JSON file, calculate SMA, and run backtest.

    Parameters:
    file_path (str): The path to the JSON file containing stock data.
    stock (str): The stock symbol being backtested ('SOXL' or 'SOXS').
    start_date (str): The start date for the backtest in 'YYYY-MM-DD' format.
    end_date (str): The end date for the backtest in 'YYYY-MM-DD' format.

    Returns:
    log_file (str): The path to the log file where backtest results are saved.
    csv_file (str): The path to the CSV file where backtest results are saved.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)

    df = parse_data(data)

    if start_date and end_date:
        df = df[start_date:end_date]

    df = calculate_sma(df)
    log, df_log = backtest(df, stock=stock)

    log_file = f"trading_log_{stock.lower()}.txt"
    csv_file = f"trading_log_{stock.lower()}.csv"

    with open(log_file, 'w') as f:
        for entry in log:
            f.write(entry + '\n')
    
    df_log.to_csv(csv_file, index=False)

    print(f"Backtesting for {stock} complete. Log saved to {log_file} and {csv_file}.")
    return log_file, csv_file

if __name__ == '__main__':
    # Run backtest for SOXL
    log_soxl, csv_soxl = run_sma_and_backtest('SOXL_data.json', 'SOXL', '2024-01-25', '2024-06-12')
    # Run backtest for SOXS
    log_soxs, csv_soxs = run_sma_and_backtest('SOXS_data.json', 'SOXS', '2024-01-25', '2024-06-12')