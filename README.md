# **COP4521-TradingBot**

## **Project Description** 
A python application that uses the Alpaca Data API and Orders API in order to trade in the background automatically. Using the Alpaca Data API we request present and historical market data, which the bot uses to make decisions on BUY/SELL orders using one of three strategies we implemented. The user has the option of which strategy they would like to run the bot with, what stock(s) they would like to trade, their buy/sell quantity, along with that strategy's specific time span parameter. Through the UI you can access previous iterations of the bot, as well as a graphical representation of your current iteration.

**TO RUN THE APP** <br />
Within the COP4521-TradingBot Directory
* Windows: 
   * > py .\venv\Scripts\activate 
   * > pip install -r .\Utility\requirements.txt  
   * > py .\app.py
* Linux: 
   * 
   * $pip install -r Utility/requirements.txt
   * $python3 app.py

### Strategies Implemented
| Simple Moving Average  |  Exponential Moving Average | Volume Trading |
|:-:|:-:|:-:|
| 5/20 Day | 12 Day  | 12 Day |
| 20/50 Day |  26 Day | 26 Day |
| 50/200 Day | 50 Day | 50 Day |

### GUI
When starting the application, you will be brought to the home dashboard. Here, there will be a listview for both the strategy you would like to run as well as which symbols you would like to trade (In order to select several symbols, use ctrl + click). Below that are three radio buttons pertaining to the time span you'd like to run, of which you can select one. You then start the bot by selecting START BOT. At this point the bot will run in the background, and can only be stopped by selecting STOP BOT. The data of 
your previous iteration will then be stored for you to view.

- - - -

### Libraries Used

* Built in Libraries
   - sys, sqlite3, datetime

* Third Party Libraries
   * alpaca-trade-api v1.4.1
   * PySide6 v6.2.1
   
**NOTE**: both third party libraries have quite a few dependencies that are not included above, but are included in our requirements.txt file.

- - - -
### Other Resoruces Used
* https://pypi.org/project/alpaca-trade-api/
* https://alpaca.markets/docs/
* https://doc.qt.io/qtforpython/

- - - -

### Work Load
* Trevor Alspach: GUI, Bot History, Bot Strategies
* James Pugh: GUI and Bot Strategies
* James Hill: Database setup, graphical representation, Bot strategies

