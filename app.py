from PySide6 import QtWidgets
from GuiWidgets.Widgets import Window
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.resize(1280,720)
    window.show()

    sys.exit(app.exec())