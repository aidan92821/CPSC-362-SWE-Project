import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from Model.model import JSONDataSource, Publisher
from View.view import DownloadDataGUI, CalendarPlotApp

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_main_gui(self):
        self.view.download_window.close()
        self.view.main_window = CalendarPlotApp(self.model.data_source, self.model.data_publisher)
        self.view.main_window.show()
        self.view.main_window.setAttribute(Qt.WA_DeleteOnClose)

    def simulate_data_change(self):
        new_data = {'ticker': 'SOXL'}
        self.model.data_publisher.notify(new_data)

    def run(self):
        app = QApplication(sys.argv)

        # Create the publisher instance
        self.model.data_publisher = Publisher()

        # Create an instance of the DownloadDataGUI with the publisher
        self.view.download_window = DownloadDataGUI(self.model.data_publisher)

        # Create the data source adapter instance
        self.model.data_source = JSONDataSource('path_to_your_json_file.json')

        # Connect the finished signal to the function to show the main GUI
        self.view.download_window.start_button.clicked.connect(self.show_main_gui)

        # Show the download window
        self.view.download_window.show()

        # Simulate a data change after some time (for demonstration purposes)
        QTimer.singleShot(5000, self.simulate_data_change)  # Simulate data change after 5 seconds

        sys.exit(app.exec_())

if __name__ == "__main__":
    model = JSONDataSource('path_to_your_json_file.json')
    view = type('View', (), {})()  # Create a dynamic object to hold views
    controller = Controller(model, view)
    controller.run()
