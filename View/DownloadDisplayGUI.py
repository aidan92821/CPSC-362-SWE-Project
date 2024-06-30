import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QComboBox, QLabel, QCalendarWidget
from PyQt5.QtCore import QDate
import os
import pandas as pd
import pyqtgraph as pg
from Model.adapterpattern import DataSourceAdapter
from Model.pubsub import Publisher, Subscriber
from Model import simpleMovingAverage

class CombinedApp(QMainWindow, Subscriber):
    def __init__(self, publisher, data_source_adapter):
        super().__init__()
        self.setWindowTitle('Data Application')
        self.setGeometry(100, 100, 1000, 600)
        
        self.publisher = publisher
        self.data_source_adapter = data_source_adapter
        self.publisher.subscribe(self)
        
        self.initUI()

    def initUI(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        self.symbol_input = QLineEdit(self)
        self.symbol_input.setPlaceholderText('Enter ticker symbol (e.g., SOXL or ETH-USD)')
        left_layout.addWidget(self.symbol_input)

        self.start_date = QCalendarWidget(self)
        self.start_date.setGridVisible(True)
        self.start_date.setMinimumDate(QDate(2021, 1, 1))
        self.start_date.setMaximumDate(QDate.currentDate())
        self.start_date.setSelectedDate(QDate(2021, 1, 1))
        left_layout.addWidget(self.start_date)

        self.end_date = QCalendarWidget(self)
        self.end_date.setGridVisible(True)
        self.end_date.setMinimumDate(QDate(2021, 1, 1))
        self.end_date.setMaximumDate(QDate.currentDate())
        self.end_date.setSelectedDate(QDate.currentDate())
        left_layout.addWidget(self.end_date)

        add_button = QPushButton('Download Data', self)
        add_button.clicked.connect(self.download_data)
        left_layout.addWidget(add_button)

        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        self.combo = QComboBox(self)
        self.combo.setPlaceholderText("Select a ticker symbol")
        self.combo.currentIndexChanged.connect(self.update_plot)
        right_layout.addWidget(self.combo)

        self.plot_widget = pg.PlotWidget(self)
        right_layout.addWidget(self.plot_widget)

        sma_button = QPushButton('Run SMA and Backtest', self)
        sma_button.clicked.connect(self.run_sma_backtest)
        right_layout.addWidget(sma_button)

        self.result_label = QLabel(self)
        right_layout.addWidget(self.result_label)

        self.update_combo_box()

    def download_data(self):
        symbol = self.symbol_input.text().strip().upper()
        start_date = self.start_date.selectedDate().toString('yyyy-MM-dd')
        end_date = self.end_date.selectedDate().toString('yyyy-MM-dd')

        if symbol in ['SOXL', 'SOXS']:
            self.data_source_adapter.download_data(symbol, start_date, end_date, f'{symbol}_data.json')
            QMessageBox.information(self, 'Success', f"Data for {symbol} downloaded successfully.")
            self.publisher.notify({'event': 'data_downloaded'})
        elif symbol in ['ETH-USD', 'BTC-USD']:
            self.data_source_adapter.download_data(symbol, start_date, end_date, f'{symbol}_data.json')
            QMessageBox.information(self, 'Success', f"Crypto data for {symbol} downloaded successfully.")
            self.publisher.notify({'event': 'data_downloaded'})
        else:
            QMessageBox.critical(self, 'Error', f"Ticker symbol '{symbol}' not recognized.")

    def update(self, data):
        if data.get('event') == 'data_downloaded':
            self.update_combo_box()
        else:
            self.result_label.setText(f"Ticker: {data['ticker']}, Price: {data['price']:.2f}")
            self.update_real_time_plot(data)

    def update_combo_box(self):
        self.combo.clear()
        stock_files = [f for f in os.listdir() if f.endswith('_data.json')]
        self.combo.addItems([f.split('_')[0] for f in stock_files])
        self.combo.setCurrentIndex(0)

    def update_plot(self):
        self.plot_widget.clear()
        ticker = self.combo.currentText()
        if ticker:
            if 'BCHARTS' in ticker:
                data = self.data_source_adapter.quandl_source.get_data(ticker, None, None)
            else:
                data = self.data_source_adapter.yfinance_source.get_data(ticker, None, None)
            data = self.format_data(data)
            if data:
                self.publisher.set_ticker(ticker, data[-1]['Close'])
                dates = [item['Date'] for item in data]
                closes = [item['Close'] for item in data]

                x = list(range(len(dates)))
                y = closes

                self.plot_widget.plot(x, y, pen='r')
            else:
                QMessageBox.critical(self, "Error", f"No data available for {ticker}.")

    def format_data(self, data):
        formatted_data = []
        for item in data:
            formatted_item = {
                "Date": item['Date'].strftime('%Y-%m-%d') if isinstance(item['Date'], pd.Timestamp) else item['Date'],
                "Open": item.get('Open'),
                "High": item.get('High'),
                "Low": item.get('Low'),
                "Close": item.get('Close'),
                "Adj Close": item.get('Adj Close'),
                "Volume": item.get('Volume')
            }
            formatted_data.append(formatted_item)
        return formatted_data

    def update_real_time_plot(self, data):
        pass

    def run_sma_backtest(self):
        ticker = self.combo.currentText()
        log_file, csv_file = simpleMovingAverage.run_sma_and_backtest(f'{ticker}_data.json', ticker)
        self.result_label.setText(f"Backtesting complete. Log saved to {log_file} and {csv_file}.")

def main():
    app = QApplication(sys.argv)
    data_source_adapter = DataSourceAdapter()
    publisher = Publisher()
    main_window = CombinedApp(publisher, data_source_adapter)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
