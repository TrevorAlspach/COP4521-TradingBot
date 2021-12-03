from PySide6 import QtWidgets, QtCharts
from PySide6.QtWidgets import *
from PySide6 import QtCore
from PySide6.QtGui import QFont
from pandas.core import frame
import TradingBot.Bot as bot


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Dashboard")
        self.centralWidget = self.setupMainWidget(MainMenu())
        self.setCentralWidget(self.centralWidget)

    def setupMainWidget(self, widget):
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.setupButtons(), 20)
        mainLayout.addWidget(widget, 80)
        widget = QWidget()
        widget.setLayout(mainLayout)
        return widget

    def setupButtons(self):
        buttonLayout = QVBoxLayout()

        button1 = QPushButton("Main Menu")
        button1.clicked.connect(self.view_main_menu)
        button2 = QPushButton("View Graph")
        button2.clicked.connect(self.view_graph)
        button3 = QPushButton("View Bot History")
        button3.clicked.connect(self.view_bot_history)
        buttonLayout.addWidget(button1)
        buttonLayout.addWidget(button2)
        buttonLayout.addWidget(button3)
        frame = QFrame()
        frame.setLayout(buttonLayout)
        frame.setFrameStyle(QFrame.Raised | QFrame.Panel)

        return frame

    def view_main_menu(self):
        self.setCentralWidget(self.setupMainWidget(MainMenu()))

    def view_bot_history(self):
        self.setCentralWidget(self.setupMainWidget(BotHistory()))

    def view_graph(self):
        self.setCentralWidget(self.setupMainWidget(self.generate_graph()))

    def generate_graph(points=None):
        series = QtCharts.QLineSeries()
        series.append(1, 1)
        series.append(2, 2)
        series.append(3, 3)
        series.append(4, 4)
        series.append(5, 5)
        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle("Example")
        chartView = QtCharts.QChartView(chart)
        return chartView


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.main_label = QLabel()
        self.main_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.main_label.setText("Welcome to the Bot!!")

        self.bot_options = QListWidget()
        self.bot_options.addItems(["SMA", "EMA", "Volume"])
        self.bot_options.setFixedSize(QtCore.QSize(300, 100))

        self.bot_symbols = QListWidget()
        self.bot_symbols.addItems(["MSFT", "AAPL", "TSLA"])
        self.bot_symbols.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.bot_symbols.setFixedSize(QtCore.QSize(300, 100))

        self.list_frame = QFrame()
        self.frame_layout = QHBoxLayout()
        self.frame_layout.addWidget(self.bot_options)
        self.frame_layout.addWidget(self.bot_symbols)
        self.list_frame.setLayout(self.frame_layout)

        self.main_button_frame = QFrame()
        self.buttonLayout = QHBoxLayout()

        self.start_button = QPushButton("START")
        self.start_button.clicked.connect(self.start_bot)
        self.stop_button = QPushButton("STOP")
        self.start_button.clicked.connect(self.stop_bot)

        self.buttonLayout.addWidget(self.start_button)
        self.buttonLayout.addWidget(self.stop_button)
        self.main_button_frame.setLayout(self.buttonLayout)

        self.layout.addWidget(self.main_label)
        self.layout.addWidget(self.list_frame)
        self.layout.addWidget(self.main_button_frame)
        self.setLayout(self.layout)

    def start_bot(self):
        strats = []
        for x in self.bot_options.selectedItems():
            print("result", x.text())

        strats = [x.text() for x in self.bot_options.selectedItems()]
        symbols = [x.text() for x in self.bot_symbols.selectedItems()]

        for strat in strats:
            if(strat == "EMA"):
                bot.runEMA(tuple(symbols), 30)
            elif(strat == "SMA"):
                bot.runSMA(tuple(symbols), 20, 50)
            elif(strat == "Volume"):
                bot.volumePrice(tuple(symbols), 30)

        self.start_button.setEnabled(False)

    def stop_bot(self):
        # Stop the Bot
        self.start_button.setEnabled(False)
        # Put bot history into database


class BotHistory(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        main_label = QLabel()
        list_view = QListView()
        main_label.setAlignment(QtCore.Qt.AlignHCenter)
        main_label.setText("Bot History Screen")

        clear_button = QPushButton()

        main_button_frame = QFrame()
        buttonLayout = QHBoxLayout()
        main_button_frame.setLayout(buttonLayout)

        layout.addWidget(main_label)
        layout.addWidget(list_view)
        layout.addWidget(main_button_frame)
        self.setLayout(layout)
