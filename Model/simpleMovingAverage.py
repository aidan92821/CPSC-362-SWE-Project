import pandas as pd
import json
import matplotlib.pyplot as plt

# Function to parse data from JSON
def parse_data(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

# Function to calculate SMA
def calculate_sma(df, short_window=20, long_window=100):
    df['STA'] = df['Adj Close'].rolling(window=short_window).mean()
    df['LTA'] = df['Adj Close'].rolling(window=long_window).mean()
    df.dropna(inplace=True)
    return df

# Function to perform backtest
def backtest(df, initial_balance=100000, stock='SOXL'):
    balance = initial_balance
    shares = 0
    log = []
    buy_sell_triggered = False
    log.append(f"{'DATE':<12}{'buy/sell':<10}{'STA':<8}{'LTA':<8}{'balance':<15}{'amount of stock':<15}")
    log.append("-" * 70)
    log_data = []

    buy_signals = []
    sell_signals = []

    for date, row in df.iterrows():
        date_str = date.strftime('%m-%d-%y')
        if stock == 'SOXL':
            if row['STA'] > row['LTA']:
                if balance > row['Adj Close']:
                    shares_to_buy = balance // row['Adj Close']
                    balance -= shares_to_buy * row['Adj Close']
                    shares += shares_to_buy
                    log.append(f"{date_str:<12}{'BUY':<10}{row['STA']:<8.2f}{row['LTA']:<8.2f}{balance:<15.2f}{shares:<15}")
                    log_data.append([date_str, 'BUY', row['STA'], row['LTA'], balance, shares])
                    buy_sell_triggered = True
                    buy_signals.append(date)
            elif row['STA'] < row['LTA'] and shares > 0:
                balance += shares * row['Adj Close']
                log.append(f"{date_str:<12}{'SELL':<10}{row['STA']:<8.2f}{row['LTA']:<8.2f}{balance:<15.2f}{shares:<15}")
                log_data.append([date_str, 'SELL', row['STA'], row['LTA'], balance, shares])
                shares = 0
                buy_sell_triggered = True
                sell_signals.append(date)
        elif stock == 'SOXS':
            if row['STA'] < row['LTA']:
                if balance > row['Adj Close']:
                    shares_to_buy = balance // row['Adj Close']
                    balance -= shares_to_buy * row['Adj Close']
                    shares += shares_to_buy
                    log.append(f"{date_str:<12}{'BUY':<10}{row['STA']:<8.2f}{row['LTA']:<8.2f}{balance:<15.2f}{shares:<15}")
                    log_data.append([date_str, 'BUY', row['STA'], row['LTA'], balance, shares])
                    buy_sell_triggered = True
                    buy_signals.append(date)
            elif row['STA'] > row['LTA'] and shares > 0:
                balance += shares * row['Adj Close']
                log.append(f"{date_str:<12}{'SELL':<10}{row['STA']:<8.2f}{row['LTA']:<8.2f}{balance:<15.2f}{shares:<15}")
                log_data.append([date_str, 'SELL', row['STA'], row['LTA'], balance, shares])
                shares = 0
                buy_sell_triggered = True
                sell_signals.append(date)

    if shares > 0:
        balance += shares * df.iloc[-1]['Adj Close']
        final_date_str = df.index[-1].strftime('%m-%d-%y')
        log.append("\n" + "-" * 70)
        log.append(f"{final_date_str:<12}{'FINAL SELL':<10}{df.iloc[-1]['STA']:<8.2f}{df.iloc[-1]['LTA']:<8.2f}{balance:<15.2f}{shares:<15}")
        log_data.append([final_date_str, 'FINAL SELL', df.iloc[-1]['STA'], df.iloc[-1]['LTA'], balance, shares])
        buy_sell_triggered = True

    if not buy_sell_triggered:
        log.append("\nNo buy or sell signals have been triggered between the dates selected.")
        log_data.append(["N/A", "N/A", "N/A", "N/A", balance, shares])

    df_log = pd.DataFrame(log_data, columns=["DATE", "buy/sell", "STA", "LTA", "balance", "amount of stock"])
    return log, df_log, buy_signals, sell_signals

# Function to run SMA and backtest
def run_sma_and_backtest(file_path, stock, start_date=None, end_date=None):
    with open(file_path, 'r') as f:
        data = json.load(f)

    df = parse_data(data)

    if start_date and end_date:
        df = df[start_date:end_date]

    df = calculate_sma(df)
    log, df_log, buy_signals, sell_signals = backtest(df, stock=stock)

    log_file = f"trading_log_{stock.lower()}.txt"
    csv_file = f"trading_log_{stock.lower()}.csv"

    with open(log_file, 'w') as f:
        for entry in log:
            f.write(entry + '\n')
    
    df_log.to_csv(csv_file, index=False)

    plot_sma_lta(df, buy_signals, sell_signals, stock)

    print(f"Backtesting for {stock} complete. Log saved to {log_file} and {csv_file}.")
    return log_file, csv_file

def plot_sma_lta(df, buy_signals, sell_signals, stock):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['STA'], label='SMA (20 days)', color='red')
    plt.plot(df.index, df['LTA'], label='LTA (100 days)', color='black')
    plt.scatter(buy_signals, df.loc[buy_signals]['Adj Close'], marker='^', color='green', label='Buy Signal', alpha=1)
    plt.scatter(sell_signals, df.loc[sell_signals]['Adj Close'], marker='v', color='red', label='Sell Signal', alpha=1)
    plt.title(f'Simple Moving Averages and Buy/Sell Signals for {stock}')
    plt.xlabel('Date')
    plt.ylabel('Adjusted Close Price')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    log_soxl, csv_soxl = run_sma_and_backtest('SOXL_data.json', 'SOXL', '2024-01-25', '2024-06-12')
    log_soxs, csv_soxs = run_sma_and_backtest('SOXS_data.json', 'SOXS', '2024-01-25', '2024-06-12')
