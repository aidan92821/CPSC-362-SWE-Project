import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QCalendarWidget, QComboBox, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QDate
import pyqtgraph as pg
from datetime import datetime
from DataAdapter import DataAdapter
import MovingAverageModel

class ChartView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_adapter = DataAdapter()
        self.setWindowTitle('PyQt5 Calendar and Plot')
        self.setGeometry(100, 100, 1000, 800)

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

    def update_combo_box(self):
        self.combo.clear()
        tickers = self.data_adapter.get_ticker_list()
        self.combo.addItems(tickers)
        if tickers:
            self.combo.setCurrentIndex(0)
            self.load_data(tickers[0])
        else:
            today = QDate.currentDate()
            self.calendar1.setSelectedDate(today)
            self.calendar2.setSelectedDate(today)

    def load_data(self, ticker):
        data = self.data_adapter.fetch_data(ticker)
        self.data = {date: info['Close'] for date, info in data.items()}
        self.update_date_range()

    def update_date_range(self):
        if not self.data:
            return

        min_date = min(self.data.keys())
        max_date = max(self.data.keys())

        self.calendar1.setMinimumDate(QDate(min_date.year, min_date.month, min_date.day))
        self.calendar1.setMaximumDate(QDate(max_date.year, max_date.month, max_date.day))
        self.calendar1.setSelectedDate(QDate(min_date.year, min_date.month, min_date.day))

        self.calendar2.setMinimumDate(QDate(min_date.year, min_date.month, min_date.day))
        self.calendar2.setMaximumDate(QDate(max_date.year, max_date.month, max_date.day))
        self.calendar2.setSelectedDate(QDate(max_date.year, max_date.month, max_date.day))

    def update_plot(self):
        self.plot_widget.clear()
        date1 = self.calendar1.selectedDate()
        date2 = self.calendar2.selectedDate()
        option = self.combo.currentText()

        py_date1 = date1.toPyDate()
        py_date2 = date2.toPyDate()

        if py_date1 > py_date2:
            py_date1, py_date2 = py_date2, py_date1

        if not option:
            return

        data = self.data_adapter.fetch_data(option, py_date1.strftime('%Y-%m-%d'), py_date2.strftime('%Y-%m-%d'))
        if not data:
            return

      

        x = [date.toordinal() for date in data.keys()]
        y = [info['Close'] for info in data.values()]

        self.plot_widget.plot(x, y, pen='r')

    def run_sma_backtest(self):
        option = self.combo.currentText()
        start_date = self.calendar1.selectedDate().toPyDate()
        end_date = self.calendar2.selectedDate().toPyDate()

        data = self.data_adapter.fetch_data(option, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

        df_log, buy_signals, sell_signals = MovingAverageModel.run_sma_and_backtest(data, option)

        log_file = f"{option}_trading_log.txt"
        csv_file = f"{option}_trading_log.csv"

        df_log.to_csv(csv_file, index=False)
        with open(log_file, 'w') as f:
            f.write(df_log.to_string())

        QMessageBox.information(self, "Backtest Complete", f"Trading log saved to {log_file}\nCSV file saved to {csv_file}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ChartView()
    main_window.show()
    sys.exit(app.exec_())
