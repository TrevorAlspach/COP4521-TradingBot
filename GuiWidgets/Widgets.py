from PySide6 import QtWidgets,QtCharts
from PySide6.QtWidgets import *
from PySide6 import QtCore
from PySide6.QtGui import QFont
from pandas.core import frame
from TradingBot.Bot import runEMA, runSMA, volumePrice, setQuantity, setQuantity, getCurrentBalance
import db.dbFunctions as db
import datetime

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

    def generate_graph(self, points=None):
        dates = db.getAnalysisDates()
        values = db.getAnaltsisValues()


        series = QtCharts.QLineSeries()

        if(len(dates)>=30):
            for x in range(0, 30):
                series.append(x, float((values[x][0])))
        else:
            for x in range (0, len(dates)):
                series.append(x, float((values[x][0])))


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

        self.options_frame = QFrame()
        self.options_layout = QVBoxLayout()
        self.options_layout.addStretch()
        self.bot_options = QListWidget()
        self.bot_options.addItems(["SMA", "EMA", "Volume"])
        self.bot_options.setFixedSize(QtCore.QSize(300, 100))
        self.strat_label = QLabel(text="Strategies")
        self.options_layout.addWidget(self.strat_label)
        self.options_layout.addWidget(self.bot_options)
        self.options_layout.addStretch()
        self.options_frame.setLayout(self.options_layout)

        self.symbols_frame = QFrame()
        self.symbols_layout = QVBoxLayout()
        self.symbols_layout.addStretch()
        self.bot_symbols = QListWidget()
        self.bot_symbols.addItems(["MSFT", "AAPL", "TSLA"])
        self.bot_symbols.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.bot_symbols.setFixedSize(QtCore.QSize(300, 100))
        self.symbols_label = QLabel(text="Symbols to Trade")
        self.symbols_layout.addWidget(self.symbols_label)
        self.symbols_layout.addWidget(self.bot_symbols)
        self.symbols_layout.addStretch()
        self.symbols_frame.setLayout(self.symbols_layout)


        self.checkbox_frame = QFrame()
        self.checkbox_label = QLabel(text= "Time Span (Days)")
        self.checkboxes = QButtonGroup()
        self.checkbox_layout = QVBoxLayout()
        self.checkbox_layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.check_1 = QRadioButton("SMA: 5, 20   EMA/Volume: 12")
        self.check_2 = QRadioButton("SMA: 20, 50   EMA/Volume: 26")
        self.check_3 = QRadioButton("SMA: 50, 200  EMA/Volume: 50")
        self.checkboxes.addButton(self.check_1)
        self.checkboxes.addButton(self.check_2)
        self.checkboxes.addButton(self.check_3)
        self.checkbox_layout.addWidget(self.checkbox_label)
        self.checkbox_layout.addWidget(self.check_1)
        self.checkbox_layout.addWidget(self.check_2)
        self.checkbox_layout.addWidget(self.check_3)
        self.checkbox_frame.setLayout(self.checkbox_layout)

        self.list_frame = QFrame()
        self.frame_layout = QHBoxLayout()
        self.frame_layout.addStretch()
        self.frame_layout.addWidget(self.options_frame)
        self.frame_layout.addWidget(self.symbols_frame)
        self.frame_layout.addStretch()
        self.list_frame.setLayout(self.frame_layout)

        self.main_button_frame = QFrame()
        self.buttonLayout = QHBoxLayout()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.whichStrategy)

        self.start_button = QPushButton("START BOT")
        self.start_button.clicked.connect(self.start_bot)
        self.stop_button = QPushButton("STOP BOT")
        self.stop_button.clicked.connect(self.stop_bot)
        self.quantity_button = QPushButton("Set Quantity")
        self.quantity_button.clicked.connect(self.set_quantity)

        self.buttonLayout.addWidget(self.start_button)
        self.buttonLayout.addWidget(self.stop_button)
        self.buttonLayout.addWidget(self.quantity_button)
        self.main_button_frame.setLayout(self.buttonLayout)

        self.layout.addWidget(self.main_label)
        self.layout.addWidget(self.list_frame)
        self.layout.addWidget(self.checkbox_frame)
        self.layout.addWidget(self.main_button_frame)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def stop_bot(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        for button in self.checkboxes.buttons():
            button.setEnabled(True)

        db.stopBotRun(datetime.datetime.now(), getCurrentBalance())

    def set_quantity(self):
        num,ok = QInputDialog.getInt(self,"Quantity Dialog","Enter Quantity")
        if ok:
            setQuantity(num)
        else:
            setQuantity(5)

    def start_bot(self):
        for x in self.bot_options.selectedItems():
            print("result", x.text())

        self.timeframe = self.checkboxes.checkedButton()
        try:
            self.strat = self.bot_options.selectedItems()[-1].text()
        except:
            print("No options selected")
        self.symbols = [x.text() for x in self.bot_symbols.selectedItems()]

        self.timer.start(21600000)
        self.start_button.setEnabled(False)
        for button in self.checkboxes.buttons():
            button.setEnabled(False)

        db.startBotRun(self.strat, datetime.datetime.now(), getCurrentBalance())

    def whichStrategy(self):
            if(self.strat == "EMA"):
                if self.timeframe == self.check_1:
                    runEMA(tuple(self.symbols), 12)
                if self.timeframe == self.check_2:
                    runEMA(tuple(self.symbols), 26)
                elif self.timeframe == self.check_3:
                    runEMA(tuple(self.symbols), 50)

            elif(self.strat == "SMA"):
                if self.timeframe == self.check_1:
                    runSMA(tuple(self.symbols), 5, 20)
                if self.timeframe == self.check_2:
                    runSMA(tuple(self.symbols), 20, 50)
                elif self.timeframe == self.check_3:
                    runSMA(tuple(self.symbols), 50, 200)

            elif(self.strat == "Volume"):
                if self.timeframe == self.check_1:
                    volumePrice(tuple(self.symbols), 12)
                if self.timeframe == self.check_2:
                    volumePrice(tuple(self.symbols), 26)
                elif self.timeframe == self.check_3:
                    volumePrice(tuple(self.symbols), 50)


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
