from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from PySide6 import QtCore
from PySide6.QtGui import QFont

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Dashboard")
        self.setCentralWidget(self.setupMainWidget())

    def setupMainWidget(self):
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.setupButtons(), 20)
        mainLayout.addWidget(QWidget(), 80)
        widget = QWidget()
        widget.setLayout(mainLayout)
        return widget
    
    def setupButtons(self):
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(QPushButton("One"))
        buttonLayout.addWidget(QPushButton("Two"))
        buttonLayout.addWidget(QPushButton("Three"))
        widget = QWidget()
        widget.setLayout(buttonLayout)
        return widget


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.Message = QLabel("Dashboard", alignment=QtCore.Qt.AlignHCenter)
        self.Message.setFont(QFont("Times New Roman", 24, QFont.Bold))

        self.buttonStart = QPushButton("Start Bot")
        self.buttonStart.setFixedSize(QtCore.QSize(350,50))
        self.buttonStop = QPushButton("Stop Bot")
        self.buttonStop.setFixedSize(QtCore.QSize(350,50))

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.Message)
        self.layout.addWidget(self.buttonStart)
        self.layout.addWidget(self.buttonStop)

