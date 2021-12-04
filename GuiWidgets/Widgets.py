from PySide6 import QtWidgets,QtCharts
from PySide6.QtWidgets import *
from PySide6 import QtCore
from TradingBot.Bot import runEMA, runSMA, volumePrice, setQuantity, addSymbol, SYMBOLS, getCurrentBalance, getPortfolioHistory
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
        button4 = QPushButton("View Bot Profit/Loss")
        button4.clicked.connect(self.view_bot_pl)
        buttonLayout.addWidget(button1)
        buttonLayout.addWidget(button2)
        buttonLayout.addWidget(button3)
        buttonLayout.addWidget(button4)
        frame = QFrame()
        frame.setLayout(buttonLayout)
        frame.setFrameStyle(QFrame.Raised | QFrame.Panel)

        return frame

    def view_bot_pl(self):
        self.setCentralWidget(self.setupMainWidget(self.generate_pl_graph()))

    def generate_pl_graph(self, points=None):
        portfolio_history = getPortfolioHistory()

        self.pl_chart = QtCharts.QChart()
        self.series = QtCharts.QLineSeries()

        count = len(portfolio_history.equity)-1
        for x in portfolio_history.equity:
            self.series.append(count, x)
            count-=1

        self.pl_chart.addSeries(self.series)
        self.pl_axis_x = QtCharts.QValueAxis()
        self.pl_axis_x.setTickCount(len(portfolio_history.equity))
        self.pl_axis_x.setReverse(True)
        self.pl_axis_x.setTitleText("Date")
        self.pl_chart.addAxis(self.pl_axis_x, QtCore.Qt.AlignBottom)
        self.series.attachAxis(self.pl_axis_x)

        self.pl_axis_y = QtCharts.QValueAxis()
        self.pl_axis_y.setTitleText("Value (in $)")
        self.pl_axis_y.setTickCount(len(portfolio_history.equity))
        self.pl_chart.addAxis(self.pl_axis_y, QtCore.Qt.AlignLeft)
        self.series.attachAxis(self.pl_axis_y)
        #self.pl_chart.addAxis(xAxis, 0)
        #self.pl_chart.addAxis(yAxis, 1)
        #self.pl_chart.createDefaultAxes()
        self.pl_chart.setTitle("Portfolio Value (last 30 days)")
        chartView = QtCharts.QChartView(self.pl_chart)

        return chartView

    def view_main_menu(self):
        self.setCentralWidget(self.setupMainWidget(MainMenu()))

    def view_bot_history(self):
        self.setCentralWidget(self.setupMainWidget(BotHistory()))

    def view_graph(self):
        self.setCentralWidget(self.setupMainWidget(self.generate_graph()))

    def generate_graph(self, points=None):
        dates = db.getAnalysisDates()
        values = db.getAnalysisValues()

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

        sym = SYMBOLS
        self.bot_symbols.addItems(sym)
        self.bot_symbols.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.bot_symbols.setFixedSize(QtCore.QSize(300, 100))
        self.symbols_label = QLabel(text="Symbols to Trade")
        self.symbols_layout.addWidget(self.symbols_label)
        self.symbols_layout.addWidget(self.bot_symbols)
        self.symbols_layout.addStretch()
        self.symbols_frame.setLayout(self.symbols_layout)

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

        self.add_symbol_button = QPushButton("Add a Symbol")
        self.add_symbol_button.clicked.connect(self.add_symbol)

        self.buttonLayout.addWidget(self.start_button)
        self.buttonLayout.addWidget(self.stop_button)
        self.buttonLayout.addWidget(self.quantity_button)
        self.buttonLayout.addWidget(self.add_symbol_button)
        self.main_button_frame.setLayout(self.buttonLayout)

        self.layout.addWidget(self.main_label)
        self.layout.addWidget(self.list_frame)
        self.layout.addWidget(self.main_button_frame)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def stop_bot(self):
        self.timer.stop()
        self.start_button.setEnabled(True)

        db.stopBotRun(datetime.datetime.now(), getCurrentBalance())

    def set_quantity(self):
        num,ok = QInputDialog.getInt(self,"Quantity Dialog","Enter Quantity")
        if ok:
            setQuantity(num)
        else:
            setQuantity(5)

    def add_symbol(self):
        text, ok = QInputDialog.getText(self, "Add Symbol Dialog", "Enter Symbol")
        if ok:
            self.bot_symbols.clear()
            self.bot_symbols.addItems(SYMBOLS)

    def start_bot(self):
        self.timeframe = 10
        self.timeframe1 = 30
        try:
            self.strat = self.bot_options.selectedItems()[-1].text()
            if(self.strat == "SMA"):
                small, ok = QInputDialog.getInt(self, "Small SMA Dialog", "Enter small SMA timeframe")
                large, ok1 = QInputDialog.getInt(self, "Large SMA Dialog", "Enter large SMA timeframe")
                if ok and ok1 and small<large:
                    self.timeframe = small
                    self.timeframe1 = large
                else:
                    self.timeframe = 10
                    self.timeframe = 30
                    print("ERROR: Large timeframe not larger than small timeframe. Setting default parameters.")

            else:
                num, ok = QInputDialog.getInt(self, "Timeframe Dialog", "Enter Timeframe")
                if ok:
                    self.timeframe = num
                else:
                    self.timeframe = 30
                    print("ERROR: Timeframe invalid. Using default parameters.")

        except:
            print("No options selected")

        self.symbols = [x.text() for x in self.bot_symbols.selectedItems()]

        self.timer.start(21600000) # change this for testing, original = 21600000

        self.start_button.setEnabled(False)

        db.startBotRun(self.strat, datetime.datetime.now(), getCurrentBalance())

    def whichStrategy(self):
            if(self.strat == "EMA"):
                runEMA(tuple(self.symbols), self.timeframe)

            elif(self.strat == "SMA"):
                runSMA(tuple(self.symbols), self.timeframe, self.timeframe1)

            elif(self.strat == "Volume"):
                volumePrice(tuple(self.symbols), self.timeframe)


class BotHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.main_label = QLabel()
        self.list_view = QListWidget()
        self.list_view.setFixedSize(1000, 200)
        self.main_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.main_label.setText("Bot History Screen")

        self.clear_button = QPushButton("Clear Bot History")
        self.clear_button.clicked.connect(self.clear_button_click)

        self.list_view.addItems(self.populate_listview())
        self.main_button_frame = QFrame()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.clear_button)
        self.main_button_frame.setLayout(self.buttonLayout)

        self.layout.addWidget(self.main_label)
        self.layout.addWidget(self.list_view)
        self.layout.addWidget(self.main_button_frame)
        self.setLayout(self.layout)

    def populate_listview(self):
        self.bot_history = db.getBotHistory()
        self.item_titles = []
        for item in self.bot_history:
            self.item_titles.append("|   STRATEGY:     " + item[0] + "   |   START:     " + item[1] + "  |   END:     " + item[2] + "  |   PROFIT:    $" + str(item[5]) + "  |  ")

        return self.item_titles

    def clear_button_click(self):
        db.clearBotHistory()
        self.list_view.clear()
