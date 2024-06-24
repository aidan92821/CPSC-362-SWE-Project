# Auto Trader Project - CPSC 362

## Overview
This project allows users to download stock data, perform simple moving average (SMA) calculations, and backtest trading strategies. The application is divided into two main functionalities: data download and analysis.

## Usage

### 1. Download Stock Data
1. Run `main.py` to start the application.
2. In the `Download Stock Data` window, enter the ticker symbol (e.g., SOXL).
3. Select the start and end dates using the calendar widgets.
4. Click "Add Ticker Symbol" to download the data.
5. Click "Finish Downloads" once all desired data is downloaded.

### 2. Analyze Data
1. After finishing downloads, the `Calendar and Plot` window will open.
2. Select the ticker symbol from the dropdown menu.
3. Use the calendar widgets to choose the date range for analysis.
4. Click "Run SMA and Backtest" to perform the analysis.
5. View the results and plot on the interface.
6. Click "Close" to exit the application.

## Requirements
- Python 3.x
- PyQt5
- yfinance
- pandas
- pyqtgraph

## Files
- `main.py`: Entry point for the application.
- `download_data_gui.py`: GUI for downloading stock data.
- `GUI.py`: GUI for analyzing stock data.
- `download_data.py`: Script for downloading stock data.
- `simpleMovingAverage.py`: Contains functions for SMA calculation and backtesting.

## Notes
- Ensure `requirements.txt` is installed using `pip install -r requirements.txt`.
- The application requires an internet connection to fetch stock data from Yahoo Finance.

Enjoy analyzing your stock data!