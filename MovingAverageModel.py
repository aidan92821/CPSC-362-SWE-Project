import pandas as pd
import matplotlib.pyplot as plt

def parse_data(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

def calculate_sma(df, short_window=20, long_window=100):
    df['STA'] = df['Adj Close'].rolling(window=short_window).mean()
    df['LTA'] = df['Adj Close'].rolling(window=long_window).mean()
    df.dropna(inplace=True)
    return df

def backtest(df, initial_balance=100000, stock='SOXL'):
    balance = initial_balance
    shares = 0
    log = []
    buy_signals = []
    sell_signals = []
    log_data = []

    for date, row in df.iterrows():
        if stock == 'SOXL' and row['STA'] > row['LTA']:
            if balance > row['Adj Close']:
                shares_to_buy = balance // row['Adj Close']
                balance -= shares_to_buy * row['Adj Close']
                shares += shares_to_buy
                log_data.append([date, 'BUY', row['STA'], row['LTA'], balance, shares])
                buy_signals.append(date)
        elif stock == 'SOXS' and row['STA'] < row['LTA']:
            if balance > row['Adj Close']:
                shares_to_buy = balance // row['Adj Close']
                balance -= shares_to_buy * row['Adj Close']
                shares += shares_to_buy
                log_data.append([date, 'BUY', row['STA'], row['LTA'], balance, shares])
                buy_signals.append(date)
        elif shares > 0:
            balance += shares * row['Adj Close']
            log_data.append([date, 'SELL', row['STA'], row['LTA'], balance, shares])
            sell_signals.append(date)
            shares = 0

    df_log = pd.DataFrame(log_data, columns=["DATE", "buy/sell", "STA", "LTA", "balance", "amount of stock"])
    return df_log, buy_signals, sell_signals

def run_sma_and_backtest(data, stock):
    df = parse_data(data)
    df = calculate_sma(df)
    df_log, buy_signals, sell_signals = backtest(df, stock=stock)
    return df_log, buy_signals, sell_signals

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
