import sys
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from download_data_gui import DownloadDataGUI
from GUI import CalendarPlotApp
from pubsub import Publisher

class DataSourceInterface:
    def get_data(self, ticker):
        raise NotImplementedError("This method should be overridden.")

class JSONDataSource(DataSourceInterface):
    def __init__(self, file_path):
        self.file_path = file_path

    def get_data(self, ticker):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data.get(ticker, None)

def main():
    app = QApplication(sys.argv)

    # Create the publisher instance
    data_publisher = Publisher()

    # Create an instance of the DownloadDataGUI
    download_window = DownloadDataGUI(data_publisher)

    # Create the data source adapter instance
    data_source = JSONDataSource('path_to_your_json_file.json')



    # Function to show the main GUI after downloads are finished
    def show_main_gui():
        # Close the download window
        download_window.close()
        # Create and show the main GUI window
        main_window = CalendarPlotApp(data_source,data_publisher)
        main_window.show()
        main_window.setAttribute(Qt.WA_DeleteOnClose)  # Ensure the window can be closed

    # Connect the finished signal to the function to show the main GUI
    download_window.finished.connect(show_main_gui)

    # Show the download window
    download_window.show()

    # Simulate data change and notify subscribers
    def simulate_data_change():
        # Simulate data change and notify subscribers
        new_data = {'ticker': 'SOXL'}
        data_publisher.notify(new_data)

    # Simulate a data change after some time (for demonstration purposes)
    QTimer.singleShot(5000, simulate_data_change)  # Simulate data change after 5 seconds    

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()