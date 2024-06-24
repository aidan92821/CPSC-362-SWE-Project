import sys
from PyQt5.QtWidgets import QApplication
from download_data_gui import DownloadDataGUI
from GUI import CalendarPlotApp

def main():
    app = QApplication(sys.argv)

    # Create an instance of the DownloadDataGUI
    download_window = DownloadDataGUI()

    # Function to show the main GUI after downloads are finished
    def show_main_gui():
        # Close the download window
        download_window.close()
        # Create and show the main GUI window
        main_window = CalendarPlotApp()
        main_window.show()
        
        # Ensure the application continues running until all windows are closed
        app.exec_()

    # Connect the finished signal to the function to show the main GUI
    download_window.finished.connect(show_main_gui)

    # Show the download window
    download_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
