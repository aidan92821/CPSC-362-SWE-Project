import sys
import json
import os
from datetime import datetime, timedelta
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QCalendarWidget, QComboBox, QHBoxLayout, QPushButton, QLabel, QMessageBox, QTextEdit
from PyQt5.QtCore import QDate
import pyqtgraph as pg
import simpleMovingAverage
from pubsub import Subscriber

class CalendarPlotApp(QMainWindow, Subscriber):
    def __init__(self, data_source, publisher, parent=None):
        super().__init__(parent)
        self.setWindowTitle('PyQt5 Calendar and Plot')
        self.setGeometry(100, 100, 1000, 800)
        self.data_source = data_source
        self.publisher = publisher
        self.publisher.subscribe(self)
        self.initUI()

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        cal_layout = QHBoxLayout()

        self.calendar1 = QCalendarWidget(self)
        self.calendar1.setGridVisible(True)
        self.calendar1.clicked[QDate].connect(self.update_plot)
        cal_layout.addWidget(self.calendar1)

        self.calendar2 = QCalendarWidget(self)
        self.calendar2.setGridVisible(True)
        self.calendar2.clicked[QDate].connect(self.update_plot)
        cal_layout.addWidget(self.calendar2)

        layout.addLayout(cal_layout)

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
        self.update_plot()


    def initUI(self):
        self.setWindowTitle('Stock Data Viewer')
        self.setGeometry(100, 100, 600, 400)

        # Create the central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add a label to display the ticker symbol
        self.ticker_label = QLabel('Ticker Symbol: ', self)
        layout.addWidget(self.ticker_label)

        # Add a text area to display the stock data
        self.data_display = QTextEdit(self)
        self.data_display.setReadOnly(True)
        layout.addWidget(self.data_display)

    def update(self, data):
        # This method will be called whenever the publisher notifies subscribers
        self.update_data_display(data['ticker'])

    def update_data_display(self, ticker):
        data = self.data_source.get_data(ticker)
        # Update the GUI with the new data
        print("Data for", ticker, ":", data)    


    def closeEvent(self, event):
        self.publisher.unsubscribe(self)
        super().closeEvent(event)

    def update_combo_box(self):
        self.combo.clear()
        stock_files = [f for f in os.listdir() if f.endswith('_data.json')]
        self.combo.addItems([f.split('_')[0] for f in stock_files])
        self.combo.setCurrentIndex(-1)
        if stock_files:
            self.load_data(stock_files[0])
        else:
            today = QDate.currentDate()
            self.calendar1.setSelectedDate(today)
            self.calendar2.setSelectedDate(today)

    def load_data(self, filename):
        with open(filename, 'r') as f:
            data_list = json.load(f)
        self.data = {datetime.strptime(item['Date'], '%Y-%m-%d').date(): item['Close'] for item in data_list}
        self.update_date_range()

    def update_date_range(self):
        if not self.data:
            return

        min_date = min(self.data.keys())
        max_date = max(self.data.keys())

        self.calendar1.setMinimumDate(QDate(2021, 1, 1))
        self.calendar1.setMaximumDate(QDate(max_date.year, max_date.month, max_date.day))
        self.calendar1.setSelectedDate(QDate(min_date.year, min_date.month, min_date.day))

        self.calendar2.setMinimumDate(QDate(2021, 1, 1))
        self.calendar2.setMaximumDate(QDate(max_date.year, max_date.month, max_date.day))
        self.calendar2.setSelectedDate(QDate(max_date.year, max_date.month, max_date.day))

    def update_plot(self):
        self.plot_widget.clear()
        if self.combo.currentIndex() == -1:
            return

        date1 = self.calendar1.selectedDate()
        date2 = self.calendar2.selectedDate()
        option = self.combo.currentText()

        py_date1 = date1.toPyDate()
        py_date2 = date2.toPyDate()

        if py_date1 > py_date2:
            py_date1, py_date2 = py_date2, py_date1

        with open(f"{option}_data.json", 'r') as f:
            data_list = json.load(f)
        
        data = {datetime.strptime(item['Date'], '%Y-%m-%d').date(): item['Close'] for item in data_list}

        min_date = min(data.keys())
        max_date = max(data.keys())

        if py_date1 < min_date or py_date2 > max_date:
            QMessageBox.critical(self, "Error", f"Please select dates between {min_date.strftime('%Y-%m-%d')} and {max_date.strftime('%Y-%m-%d')} for {option}.")
            return

        x = []
        y = []
        current_date = py_date1
        while current_date <= py_date2:
            if current_date in data:
                x.append(current_date)
                y.append(data[current_date])
            current_date += timedelta(days=1)

        x = [i for i in range(len(x))]
        self.plot_widget.plot(x, y, pen='r')

    def run_sma_backtest(self):
        option = self.combo.currentText()

        if not option:
            QMessageBox.critical(self, "Error", "No ticker symbol selected.")
            return

        date1 = self.calendar1.selectedDate()
        date2 = self.calendar2.selectedDate()
        
        start_date = date1.toPyDate().strftime('%Y-%m-%d')
        end_date = date2.toPyDate().strftime('%Y-%m-%d')

        log_file, csv_file = simpleMovingAverage.run_sma_and_backtest(f'{option}_data.json', option, start_date, end_date)

        self.result_label.setText(f"Backtesting complete. Log saved to {log_file} and {csv_file}.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = CalendarPlotApp()
    main_window.show()
    sys.exit(app.exec_())
