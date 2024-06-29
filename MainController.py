import sys
from PyQt5.QtWidgets import QApplication
from DownloadDataGUI import DownloadDataGUI
from ChartView import ChartView

def main():
    app = QApplication(sys.argv)

    download_window = DownloadDataGUI()

    def show_main_gui():
        download_window.close()
        main_window = ChartView()
        main_window.show()

    download_window.finished.connect(show_main_gui)
    download_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
