import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel, QMessageBox, QPushButton
from Model import simpleMovingAverage
import pyqtgraph as pg
from Model.model import JSONDataSource
from Model.pubsub import Subscriber, Publisher



class DataViewerApp(QMainWindow, Subscriber):
    def __init__(self, data_source, publisher, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Stock Data Viewer')
        self.setGeometry(100, 100, 800, 600)
        self.data_source = data_source
        self.publisher = publisher
        self.publisher.subscribe(self)
        self.initUI()

    def initUI(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.combo = QComboBox(self)
        self.combo.setPlaceholderText("Select a ticker symbol")
        self.combo.currentIndexChanged.connect(self.update_plot)
        layout.addWidget(self.combo)

        self.plot_widget = pg.PlotWidget(self)
        layout.addWidget(self.plot_widget)

        self.sma_button = QPushButton('Run SMA and Backtest', self)
        self.sma_button.clicked.connect(self.run_sma_backtest)
        layout.addWidget(self.sma_button)

        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        self.update_combo_box()

    def update(self, data):
        self.result_label.setText(f"Ticker: {data['ticker']}, Price: {data['price']:.2f}")

    def update_combo_box(self):
        self.combo.clear()
        stock_files = [f for f in os.listdir() if f.endswith('_data.json')]
        self.combo.addItems([f.split('_')[0] for f in stock_files])
        self.combo.setCurrentIndex(0)
        self.update_plot()

    def update_plot(self):
        self.plot_widget.clear()
        ticker = self.combo.currentText()
        data = self.data_source.get_data(ticker)

        if data:
            self.publisher.set_ticker(ticker, data[-1]['Close'])  # Set the initial price
            dates = [item['Date'] for item in data]
            closes = [item['Close'] for item in data]

            x = list(range(len(dates)))
            y = closes

            self.plot_widget.plot(x, y, pen='r')
        else:
            QMessageBox.critical(self, "Error", f"No data available for {ticker}.")

    def run_sma_backtest(self):
        ticker = self.combo.currentText()
        # Implement your SMA and backtest logic here
        log_file, csv_file = simpleMovingAverage.run_sma_and_backtest(f'{ticker}_data.json', ticker)
        self.result_label.setText(f"Backtesting complete. Log saved to {log_file} and {csv_file}.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data_source = JSONDataSource('.')  # Base path for the JSON files
    publisher = Publisher()
    main_window = DataViewerApp(data_source, publisher)
    main_window.show()
    sys.exit(app.exec_())
