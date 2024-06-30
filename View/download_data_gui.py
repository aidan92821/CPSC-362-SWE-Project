import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QCalendarWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QDate, pyqtSignal
import Model.download_data as download_data
from Model.pubsub import Publisher

class DownloadDataGUI(QMainWindow):
    """
    A class to represent the GUI for downloading stock data.
    
    Attributes
    ----------
    finished : pyqtSignal
        A custom signal emitted when the "Finish Downloads" button is clicked.
    
    Methods
    -------
    __init__():
        Constructs the necessary attributes for the GUI object.
    initUI():
        Initializes the user interface.
    download_data():
        Downloads the stock data based on user input and saves it as a JSON file.
    finish_downloads():
        Emits the finished signal and closes the GUI.
    """
    
    finished = pyqtSignal()

    def __init__(self, publisher):
        """Constructs all the necessary attributes for the GUI object."""
        super().__init__()
        self.setWindowTitle('Download Stock Data')
        self.setGeometry(100, 100, 300, 300)
        self.publisher = publisher
        self.initUI()

    def initUI(self):
        """Initializes the user interface by setting up widgets and layouts."""
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Input field for ticker symbol
        self.symbol_input = QLineEdit(self)
        self.symbol_input.setPlaceholderText('Enter ticker symbol (e.g., SOXL)')
        layout.addWidget(self.symbol_input)

        # Calendar widget for start date selection
        self.start_date = QCalendarWidget(self)
        self.start_date.setGridVisible(True)
        self.start_date.setMinimumDate(QDate(2021, 1, 1))  # Minimum date set to January 1, 2021
        self.start_date.setMaximumDate(QDate.currentDate())
        self.start_date.setSelectedDate(QDate(2021, 1, 1))
        layout.addWidget(self.start_date)

        # Calendar widget for end date selection
        self.end_date = QCalendarWidget(self)
        self.end_date.setGridVisible(True)
        self.end_date.setMinimumDate(QDate(2021, 1, 1))  # Minimum date set to January 1, 2021
        self.end_date.setMaximumDate(QDate.currentDate())
        self.end_date.setSelectedDate(QDate.currentDate())
        layout.addWidget(self.end_date)

        # Button to add ticker symbol and download data
        add_button = QPushButton('Add Ticker Symbol', self)
        add_button.clicked.connect(self.download_data)
        layout.addWidget(add_button)

        # Button to finish downloads and close the GUI
        self.finish_button = QPushButton('Finish Downloads', self)
        self.finish_button.clicked.connect(self.finish_downloads)
        layout.addWidget(self.finish_button)

    def download_data(self):
        """
        Downloads the stock data based on user input and saves it as a JSON file.
        Displays an error message if the ticker symbol is invalid or the data cannot be fetched.
        """
        symbol = self.symbol_input.text().strip().upper()
        if symbol not in ['SOXL', 'SOXS']:
            QMessageBox.critical(self, 'Error', f"Sorry, '{symbol}' is not able to be fetched. Please try another ticker symbol.")
            return
        
        start_date = self.start_date.selectedDate().toString('yyyy-MM-dd')
        end_date = self.end_date.selectedDate().toString('yyyy-MM-dd')

        try:
            data = download_data.download_stock_data(symbol, start_date, end_date)
            download_data.save_to_json(data, f"{symbol}_data.json")
            self.symbol_input.clear()
            QMessageBox.information(self, 'Success', f"Data for {symbol} downloaded successfully.")
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

    def finish_downloads(self):
        """Emits the finished signal and closes the GUI."""
        self.finished.emit()
        self.close()

class DataSourceAdapter:
    def __init__(self, download_function, save_function):
        self.download_function = download_function
        self.save_function = save_function

    def download_data(self, symbol, start_date, end_date):
        # Implementation of how to adapt download_function to DataSource interface
        return self.download_function(symbol, start_date, end_date)

    def save_data(self, data, file_name):
        # Implementation of how to adapt save_function to DataSource interface
        self.save_function(data, file_name)

        
class DataSource:
    def __init__(self, initial_data=None):
        self._data = initial_data if initial_data else {}

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data        

if __name__ == "__main__":
    publisher = Publisher()
    app = QApplication(sys.argv)
    window = DownloadDataGUI(publisher)
    window.finished.connect(app.quit)   # Ensure the application quits 
    window.show()
    sys.exit(app.exec_())