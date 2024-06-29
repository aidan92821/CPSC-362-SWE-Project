import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
import pyqtgraph as pg
from MovingAverageModel import run_sma_and_backtest, plot_sma_lta

class SMAChartView(QMainWindow):
    def __init__(self, data, stock):
        super().__init__()
        self.setWindowTitle('SMA and LMA Chart')
        self.setGeometry(100, 100, 800, 600)

        self.data, self.buy_signals, self.sell_signals = run_sma_and_backtest(data, stock)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        plot_widget = pg.PlotWidget()
        layout.addWidget(plot_widget)
        self.setCentralWidget(plot_widget)
        self.plot_data(plot_widget)

    def plot_data(self, plot_widget):
        plot_widget.plot(self.data.index, self.data['STA'], pen='r', name='SMA')
        plot_widget.plot(self.data.index, self.data['LTA'], pen='k', name='LMA')
        # Add buy/sell signals as needed

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = {}  # Replace with actual data
    stock = 'SOXL'  # Replace with actual stock symbol
    main_window = SMAChartView(data, stock)
    main_window.show()
    sys.exit(app.exec_())
