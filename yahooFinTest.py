import yfinance as yf
import json
import matplotlib.pyplot as plt
from datetime import datetime


# Fetch data for SOXL
dataSOXL = yf.download('SOXL', start='2021-01-01', end='2024-06-04')
dataSOXS = yf.download('SOXS', start='2021-01-01', end='2024-06-04')

# Plot the closing prices
plt.figure(figsize=(10, 5))
plt.plot(dataSOXL['Close'], label='SOXL Close Price')
plt.plot(dataSOXS['Close'], label='SOXS Close Price')
plt.title('SOXL & SOXS ETF Closing Prices')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()