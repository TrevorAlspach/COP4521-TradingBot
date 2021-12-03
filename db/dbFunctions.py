import sqlite3

def setUpDatabase():
    conn = sqlite3.connect('botData.db')

    conn.execute('CREATE TABLE IF NOT EXISTS Account (Username TEXT(40), Status TEXT(40), Cash TEXT(40), PortfolioValue TEXT(40))')

    conn.execute('CREATE TABLE IF NOT EXISTS Portfolio (Symbol TEXT(4), Date TIMESTAMP, Quantity INT, Price FLOAT, BuySell TEXT(4))')

    conn.execute('CREATE TABLE IF NOT EXISTS Analysis(Symbol TEXT(4), Date TEXT, Price FLOAT)')

    conn.commit()
    conn.close()

def getBotHistory():
    with sqlite3.connect('botData.db') as db:
        db.execute()

