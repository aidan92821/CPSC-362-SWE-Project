import sys
from PyQt5.QtWidgets import QApplication
from View.DownloadDisplayGUI import CombinedApp
from Model.adapterpattern import DataSourceAdapter
from Model.pubsub import Publisher

def main():
    app = QApplication(sys.argv)

    data_source_adapter = DataSourceAdapter()
    publisher = Publisher()

    main_window = CombinedApp(publisher, data_source_adapter)
    main_window.show()

    publisher.simulate_real_time_data()  # Start real-time data simulation

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
