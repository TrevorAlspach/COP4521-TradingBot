# **COP4521-TradingBot**

## **Project Plan** 
### Trading Bot
	A python script that will use the Alpaca Data API and Orders API. Information gathered from the Data API include historical and present market data, which the bot will use to make decisions on BUY/SELL orders using one of several strategies we will implement(Simple Moving Average, etc.). The user will have the option of which strategy they would like to run the bot with, plus what stock(s) they would like to trade. 

### GUI
	The bot will be accessed through a GUI. We are going to use Qt6 for python to develop the UI. This will include several widgets such as buttons to start/stop the bot, a graphical representation of the current iteration as a line chart, a list of previous orders and the current profit/loss. 

### Database
	 We are going to use an sqlite database which will have a table that records previous iterations of the bot. The schema of the table will look something similar to below:

| Symbol  |  character(5) |
| IsPaperTrade  |  BOOLEAN |
| StartTime | DATETIME  |
| EndTime  | DATETIME  |
|   |   |