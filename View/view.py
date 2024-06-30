from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton

class DownloadDataGUI(QMainWindow):
    def __init__(self, publisher):
        super().__init__()
        self.publisher = publisher
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Download Data')
        layout = QVBoxLayout()
        self.start_button = QPushButton('Start Download', self)
        layout.addWidget(self.start_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.start_button.clicked.connect(self.on_start)

    def on_start(self):
        self.publisher.notify({'status': 'started'})
        self.close()

class CalendarPlotApp(QMainWindow):
    def __init__(self, data_source, publisher):
        super().__init__()
        self.data_source = data_source
        self.publisher = publisher
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calendar Plot')
        layout = QVBoxLayout()
        self.plot_button = QPushButton('Plot Data', self)
        layout.addWidget(self.plot_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.plot_button.clicked.connect(self.on_plot)

    def on_plot(self):
        data = self.data_source.get_data('ticker')
        # plot the data
