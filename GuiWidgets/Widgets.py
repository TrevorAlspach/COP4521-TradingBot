from PySide6 import QtWidgets, QtCharts
from PySide6.QtWidgets import *
from PySide6 import QtCore
from PySide6.QtGui import QFont

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

        button1 = QPushButton("View Graph")
        button1.clicked.connect(self.view_graph)
        button2 = QPushButton("View Bot History")
        button2.clicked.connect(self.view_bot_history)
        button3 = QPushButton("Three")
        button2.clicked.connect(self.view_bot_history)
        buttonLayout.addWidget(button1)
        buttonLayout.addWidget(button2)
        buttonLayout.addWidget(button3)
        frame = QFrame()
        frame.setLayout(buttonLayout)
        frame.setFrameStyle(QFrame.Raised | QFrame.Panel)

        return frame

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

    def view_bot_history(self):
        self.setCentralWidget(self.setupMainWidget(BotHistory()))


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        main_label = QLabel()
        second_label = QLabel()
        main_label.setAlignment(QtCore.Qt.AlignHCenter)
        second_label.setAlignment(QtCore.Qt.AlignHCenter)
        main_label.setText("Welcome to the Bot!!")
        second_label.setText("Click a button to do something")

        main_button_frame = QFrame()
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(QPushButton("START"))
        buttonLayout.addWidget(QPushButton("STOP"))
        main_button_frame.setLayout(buttonLayout)


        layout.addWidget(main_label)
        layout.addWidget(second_label)
        layout.addWidget(main_button_frame)
        self.setLayout(layout)
        
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