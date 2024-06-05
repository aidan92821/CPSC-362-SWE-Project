import yfinance as yf
import json
import matplotlib.pyplot as plt
from datetime import datetime


# Fetch data for SOXL
data = yf.download('SOXL', start='2023-01-01', end='2023-12-31')

# Plot the closing prices
plt.figure(figsize=(10, 5))
plt.plot(data['Close'], label='SOXL Close Price')
plt.title('SOXL ETF Closing Prices')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()