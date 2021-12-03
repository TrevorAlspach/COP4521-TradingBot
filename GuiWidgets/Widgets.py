from PySide6 import QtWidgets, QtCharts
from PySide6.QtWidgets import *
from PySide6 import QtCore
from PySide6.QtGui import QFont
from pandas.core import frame
#import TradingBot.Bot as bot

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

    def generate_graph(points = None):
        series = QtCharts.QLineSeries()
        series.append(1,1)
        series.append(2,2)
        series.append(3,3)
        series.append(4,4)
        series.append(5,5)
        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle("Example")
        chartView = QtCharts.QChartView(chart)
        return chartView

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        main_label = QLabel()
        main_label.setAlignment(QtCore.Qt.AlignHCenter)
        main_label.setText("Welcome to the Bot!!")

        bot_options = QListWidget()
        bot_options.addItems(["SMA", "EMA", "Volume"])
        bot_options.setFixedSize(QtCore.QSize(300, 100))

        bot_symbols = QListWidget()
        bot_symbols.addItems(["MSFT", "AAPL", "TSLA"])
        bot_symbols.setSelectionMode(QAbstractItemView.ExtendedSelection)
        bot_symbols.setFixedSize(QtCore.QSize(300, 100))

        list_frame = QFrame()
        frame_layout = QHBoxLayout()
        frame_layout.addWidget(bot_options)
        frame_layout.addWidget(bot_symbols)
        list_frame.setLayout(frame_layout)

        main_button_frame = QFrame()
        buttonLayout = QHBoxLayout()

        start_button = QPushButton("START")
        start_button.clicked.connect(self.start_bot)
        stop_button = QPushButton("STOP")
        buttonLayout.addWidget(start_button)
        buttonLayout.addWidget(stop_button)
        main_button_frame.setLayout(buttonLayout)

        layout.addWidget(main_label)
        layout.addWidget(list_frame)
        layout.addWidget(main_button_frame)
        self.setLayout(layout)

    def start_bot(self):
        pass
        
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