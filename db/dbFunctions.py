import sqlite3

def setUpDatabase():
    conn = sqlite3.connect('botData.db')

    conn.execute('CREATE TABLE IF NOT EXISTS Account (Username TEXT(40), Status TEXT(40), Cash TEXT(40), PortfolioValue TEXT(40))')

    conn.execute('CREATE TABLE IF NOT EXISTS Portfolio (Symbol TEXT(4), Date DATETIME, Quantity INT, Price FLOAT, BuySell TEXT(4))')

    conn.execute('CREATE TABLE IF NOT EXISTS Analysis(Symbol TEXT(4), Date TEXT, Price FLOAT)')

    conn.execute('CREATE TABLE IF NOT EXISTS SMAAnalysis(Symbol TEXT(4), Date TEXT, LargeSMA FLOAT, SmallSMA FLOAT)')

    conn.execute('CREATE TABLE IF NOT EXISTS BotHistory(Strategy TEXT(3), StartDate DATETIME, EndDate DATETIME, StartBalance FLOAT, EndBalance FLOAT, Profit FLOAT, CurrentBot INTEGER)')

    conn.commit()
    conn.close()

def getBotHistory():
    with sqlite3.connect('botData.db') as db:
        return db.execute("SELECT * FROM BotHistory").fetchall()
    
def clearBotHistory():
     with sqlite3.connect('botData.db') as db:
         db.execute("DELETE FROM BotHistory WHERE CurrentBot = 0")

def startBotRun(strategy, start_date, start_balance):
      with sqlite3.connect('botData.db') as db:
          db.execute("INSERT INTO BotHistory(Strategy, StartDate, StartBalance, CurrentBot) VALUES (?,?,?,?)", (strategy, start_date, start_balance, 1))

def stopBotRun(end_date, end_balance):
    with sqlite3.connect('botData.db') as db:
        start_balance = db.execute("SELECT StartBalance FROM BotHistory WHERE CurrentBot = 1").fetchone()[0]
        profit = float(end_balance) - float(start_balance)
        db.execute("UPDATE BotHistory SET (EndDate, EndBalance, Profit, CurrentBot) = (?,?,?,?) WHERE CurrentBot = 1", (end_date, end_balance, profit, 0))

def getAnalysisDates():
    with sqlite3.connect('botData.db') as db:
        curr = db.cursor()
        Dates = curr.execute('SELECT Date FROM Analysis LIMIT 0, 30').fetchall()
        return Dates

def getAnalysisValues():
    with sqlite3.connect('botData.db') as db:
        curr = db.cursor()
        Values = curr.execute('SELECT Price FROM Analysis LIMIT 0, 30').fetchall()
        return Values

