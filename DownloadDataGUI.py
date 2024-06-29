import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QCalendarWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QDate, pyqtSignal
from DataAdapter import DataAdapter

class DownloadDataGUI(QMainWindow):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Download Stock Data')
        self.setGeometry(100, 100, 300, 300)
        self.data_adapter = DataAdapter()  # Use DataAdapter
        self.initUI()

    def initUI(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.symbol_input = QLineEdit(self)
        self.symbol_input.setPlaceholderText('Enter ticker symbol (e.g., SOXL)')
        layout.addWidget(self.symbol_input)

        self.start_date = QCalendarWidget(self)
        self.start_date.setGridVisible(True)
        self.start_date.setMinimumDate(QDate(2021, 1, 1))
        self.start_date.setMaximumDate(QDate.currentDate())
        self.start_date.setSelectedDate(QDate(2021, 1, 1))
        layout.addWidget(self.start_date)

        self.end_date = QCalendarWidget(self)
        self.end_date.setGridVisible(True)
        self.end_date.setMinimumDate(QDate(2021, 1, 1))
        self.end_date.setMaximumDate(QDate.currentDate())
        self.end_date.setSelectedDate(QDate.currentDate())
        layout.addWidget(self.end_date)

        add_button = QPushButton('Add Ticker Symbol', self)
        add_button.clicked.connect(self.download_data)
        layout.addWidget(add_button)

        self.finish_button = QPushButton('Finish Downloads', self)
        self.finish_button.clicked.connect(self.finish_downloads)
        layout.addWidget(self.finish_button)

    def download_data(self):
        symbol = self.symbol_input.text().strip().upper()
        if symbol not in ['SOXL', 'SOXS']:
            QMessageBox.critical(self, 'Error', f"Sorry, '{symbol}' is not able to be fetched. Please try another ticker symbol.")
            return
        
        start_date = self.start_date.selectedDate().toString('yyyy-MM-dd')
        end_date = self.end_date.selectedDate().toString('yyyy-MM-dd')

        try:
            self.data_adapter.download_and_save(symbol, start_date, end_date)  # Use adapter
            self.symbol_input.clear()
            QMessageBox.information(self, 'Success', f"Data for {symbol} downloaded successfully.")
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

    def finish_downloads(self):
        self.finished.emit()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloadDataGUI()
    window.finished.connect(app.quit)
    window.show()
    sys.exit(app.exec_())
