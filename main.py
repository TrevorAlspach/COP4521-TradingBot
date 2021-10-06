from PySide6 import QtWidgets
import sys

from GuiWidgets.AppWidget import AppWidget


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    mainPage = AppWidget()
    mainPage.resize(1280,720)
    mainPage.show()

    sys.exit(app.exec())