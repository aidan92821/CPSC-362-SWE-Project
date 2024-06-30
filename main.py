import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from View.download_data_gui import DownloadDataGUI
from View.GUI import DataViewerApp
from Model.pubsub import Publisher
from Model.model import JSONDataSource

def main():
    app = QApplication(sys.argv)

    data_publisher = Publisher()

    download_window = DownloadDataGUI(data_publisher)
    data_source = JSONDataSource('.')  # Base path for the JSON files

    def show_main_gui():
        download_window.close()
        main_window = DataViewerApp(data_source, data_publisher)
        main_window.show()
        main_window.setAttribute(Qt.WA_DeleteOnClose)

    download_window.finished.connect(show_main_gui)

    download_window.show()

    data_publisher.simulate_real_time_data()  # Start simulation

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
