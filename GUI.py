import sys
import json
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QCalendarWidget, QComboBox, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QDate
import pyqtgraph as pg
from datetime import datetime, timedelta
import simpleMovingAverage

class CalendarPlotApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load data from JSON files
        with open('SOXL_data.json', 'r') as f:
            soxl_list = json.load(f)

        with open('SOXS_data.json', 'r') as f:
            soxs_list = json.load(f)

        # Convert list to dictionary with date as key for easier lookup
        self.soxl_data = {datetime.strptime(item['Date'], '%Y-%m-%d').date(): item['Close'] for item in soxl_list}
        self.soxs_data = {datetime.strptime(item['Date'], '%Y-%m-%d').date(): item['Close'] for item in soxs_list}

        # Set up the main window properties
        self.setWindowTitle('PyQt5 Calendar and Plot')
        self.setGeometry(100, 100, 1000, 800)

        # Create the main widget and set it as the central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create a vertical layout for the main widget
        layout = QVBoxLayout(main_widget)

        # Create a horizontal layout for the calendar widgets
        cal_layout = QHBoxLayout()

        # Create and configure the first calendar widget
        self.calendar1 = QCalendarWidget(self)
        self.calendar1.setGridVisible(True)
        self.calendar1.clicked[QDate].connect(self.update_plot)

        # Create and configure the second calendar widget
        self.calendar2 = QCalendarWidget(self)
        self.calendar2.setGridVisible(True)
        self.calendar2.clicked[QDate].connect(self.update_plot)

        # Set the minimum and maximum dates for the calendars based on the data
        min_date = min(self.soxl_data.keys())
        max_date = max(self.soxl_data.keys())
        self.calendar1.setMinimumDate(QDate(min_date.year, min_date.month, min_date.day))
        self.calendar1.setMaximumDate(QDate(max_date.year, max_date.month, max_date.day))
        self.calendar2.setMinimumDate(QDate(min_date.year, min_date.month, min_date.day))
        self.calendar2.setMaximumDate(QDate(max_date.year, max_date.month, max_date.day))

        # Add the calendar widgets to the horizontal layout
        cal_layout.addWidget(self.calendar1)
        cal_layout.addWidget(self.calendar2)
        layout.addLayout(cal_layout)

        # Create a dropdown menu for selecting between SOXL and SOXS
        self.combo = QComboBox(self)
        self.combo.addItem("SOXL")
        self.combo.addItem("SOXS")
        self.combo.currentIndexChanged.connect(self.update_plot)

        # Add the dropdown menu to the vertical layout
        layout.addWidget(self.combo)

        # Create a plot widget using pyqtgraph and add it to the vertical layout
        self.plot_widget = pg.PlotWidget(self)
        layout.addWidget(self.plot_widget)

        # Create a button to run the Simple Moving Average (SMA) calculation and backtest
        self.sma_button = QPushButton('Run SMA and Backtest', self)
        self.sma_button.clicked.connect(self.run_sma_backtest)
        layout.addWidget(self.sma_button)

        # Create a label to display the results of the SMA and backtest
        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        # Initial plot to display upon launching the application
        self.update_plot()

    def update_plot(self):
        """
        Update the plot based on the selected dates and the selected stock (SOXL or SOXS).
        """
        self.plot_widget.clear()
        
        # Get the selected dates from the calendars
        date1 = self.calendar1.selectedDate()
        date2 = self.calendar2.selectedDate()
        option = self.combo.currentText()
        
        # Convert QDate to Python date
        py_date1 = date1.toPyDate()
        py_date2 = date2.toPyDate()
        
        # Ensure the start date is before the end date
        if py_date1 > py_date2:
            py_date1, py_date2 = py_date2, py_date1

        # Select the correct data based on the dropdown option
        if option == "SOXL":
            data = self.soxl_data
        else:
            data = self.soxs_data

        # Extract data points within the selected date range
        x = []
        y = []
        current_date = py_date1
        while current_date <= py_date2:
            if current_date in data:
                x.append(current_date)
                y.append(data[current_date])
            current_date += timedelta(days=1)

        # Convert dates to a numerical format for plotting
        x = [i for i in range(len(x))]
        
        # Plot the data
        self.plot_widget.plot(x, y, pen='r')

    def run_sma_backtest(self):
        """
        Run the SMA and backtest the strategy based on the selected stock (SOXL or SOXS).
        """
        option = self.combo.currentText()

        # Get the selected dates from the calendars
        date1 = self.calendar1.selectedDate()
        date2 = self.calendar2.selectedDate()
        
        # Convert QDate to Python date
        start_date = date1.toPyDate().strftime('%Y-%m-%d')
        end_date = date2.toPyDate().strftime('%Y-%m-%d')

        # Run SMA and backtest using the function from simpleMovingAverage.py
        log_file, csv_file = simpleMovingAverage.run_sma_and_backtest(f'{option}_data.json', option, start_date, end_date)

        # Update the result label with a completion message
        self.result_label.setText(f"Backtesting complete. Log saved to {log_file} and {csv_file}.")

if __name__ == '__main__':
    # Create an instance of the application
    app = QApplication(sys.argv)
    main_window = CalendarPlotApp()
    main_window.show()
    sys.exit(app.exec_())
