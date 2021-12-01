import sqlite3

def setUpDatabase():
    conn = sqlite3.connect('botData.db')
    conn.close()

def getBotHistory():
    with sqlite3.connect('botData.db') as db:
        db.execute()