import sys
import json
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
import pyqtgraph as pg
from datetime import datetime

class SMAPlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SMA and LTA Plot')
        self.setGeometry(100, 100, 1000, 800)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.plot_widget = pg.PlotWidget(self)
        layout.addWidget(self.plot_widget)

        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        self.plot_data()

    def plot_data(self):
        self.plot_widget.clear()

        # Load the data from the JSON files
        with open('SOXL_data.json', 'r') as f:
            soxl_list = json.load(f)
        with open('SOXS_data.json', 'r') as f:
            soxs_list = json.load(f)

        # Convert lists to DataFrames
        soxl_df = pd.DataFrame(soxl_list)
        soxs_df = pd.DataFrame(soxs_list)

        # Convert 'Date' column to datetime
        soxl_df['Date'] = pd.to_datetime(soxl_df['Date'])
        soxs_df['Date'] = pd.to_datetime(soxs_df['Date'])

        # Calculate SMA and LTA
        soxl_df['SMA'] = soxl_df['Close'].rolling(window=20).mean()
        soxl_df['LTA'] = soxl_df['Close'].rolling(window=100).mean()
        soxs_df['SMA'] = soxs_df['Close'].rolling(window=20).mean()
        soxs_df['LTA'] = soxs_df['Close'].rolling(window=100).mean()

        # Plot SOXL data
        self.plot_widget.plot(soxl_df['Date'], soxl_df['SMA'], pen='r', name='SOXL SMA')
        self.plot_widget.plot(soxl_df['Date'], soxl_df['LTA'], pen='b', name='SOXL LTA')

        # Plot SOXS data
        self.plot_widget.plot(soxs_df['Date'], soxs_df['SMA'], pen='g', name='SOXS SMA')
        self.plot_widget.plot(soxs_df['Date'], soxs_df['LTA'], pen='k', name='SOXS LTA')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SMAPlotApp()
    main_window.show()
    sys.exit(app.exec_())
