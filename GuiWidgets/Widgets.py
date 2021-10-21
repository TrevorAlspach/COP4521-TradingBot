from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtGui import QFont

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()



class AppWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.Message = QtWidgets.QLabel("Dashboard", alignment=QtCore.Qt.AlignHCenter)
        self.Message.setFont(QFont("Times New Roman", 24, QFont.Bold))

        self.buttonStart = QtWidgets.QPushButton("Start Bot")
        self.buttonStart.setFixedSize(QtCore.QSize(350,50))
        self.buttonStop = QtWidgets.QPushButton("Stop Bot")
        self.buttonStop.setFixedSize(QtCore.QSize(350,50))

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.Message)
        self.layout.addWidget(self.buttonStart)
        self.layout.addWidget(self.buttonStop)