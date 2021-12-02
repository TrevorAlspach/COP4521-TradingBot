from PySide6 import QtWidgets
from GuiWidgets.Widgets import Window
import sys
import TradingBot.Bot as Bot
import db.dbFunctions as db


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    db.setUpDatabase()

    window = Window()
    window.resize(1280,720)
    window.show()
    #Bot.runSMA(("AAPL", "MSFT"), 20, 50)
    #Bot.volumePrice(("AAPL", "MSFT"), 30)
    #Bot.runEMA(("AAPL", "MSFT"), 50)
    sys.exit(app.exec())
