import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def fetch_and_plot_data():
    # Get the ticker symbols from the entry widgets
    ticker1 = entry1.get()
    ticker2 = entry2.get()
    
    # Fetch data for the input tickers
    try:
        data1 = yf.download(ticker1, start='2021-01-01', end=datetime.today().strftime('%Y-%m-%d'))
        data2 = yf.download(ticker2, start='2021-01-01', end=datetime.today().strftime('%Y-%m-%d'))
        
        if data1.empty or data2.empty:
            raise ValueError("One or both of the ticker symbols are invalid.")
        
        # Plot the closing prices
        plt.figure(figsize=(10, 5))
        plt.plot(data1['Close'], label=f'{ticker1.upper()} Close Price')
        plt.plot(data2['Close'], label=f'{ticker2.upper()} Close Price')
        plt.title(f'{ticker1.upper()} & {ticker2.upper()} ETF Closing Prices')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Stock Ticker Input")

# Create and place the labels and entry widgets
tk.Label(root, text="Enter the first ticker symbol:").grid(row=0, column=0, padx=10, pady=10)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Enter the second ticker symbol:").grid(row=1, column=0, padx=10, pady=10)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=10, pady=10)

# Create and place the button
button = tk.Button(root, text="Fetch and Plot Data", command=fetch_and_plot_data)
button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the main event loop
root.mainloop()