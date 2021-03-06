from datetime import datetime, timedelta
import alpaca_trade_api as alpacaAPI
import numpy
from alpaca_trade_api.rest import APIError, TimeFrame
from TradingBot.config import *
import db.dbFunctions as db
import logging
import sqlite3 as sql

BASE_URL = "https://paper-api.alpaca.markets"

api = alpacaAPI.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
account = api.get_account()
QUANTITY = 5
SYMBOLS = ["MSFT", "AAPL", "TSLA", "AMZN", "FB"]

def runSMA(symbols, smallSMASize, largeSMASize):
    print(f"Running SMA on {symbols} with sizes {smallSMASize} and {largeSMASize}")
    if account.status != "ACTIVE":
        logging.error("Alpaca Account is not able to trade")
        return False
    symbolsToTrade = symbols

    currentDate = datetime.today().date() - timedelta(
        days=1)  # Since we are going to use close data, use the previous days close
    startDate = currentDate - timedelta(days=100)

    for symbol in symbolsToTrade:
        bars = api.get_bars(symbol, TimeFrame.Day, start=startDate, end=currentDate, limit=100).df

        largeSMA = bars.close.rolling(largeSMASize).mean()[-1]
        smallSMA = bars.close.rolling(smallSMASize).mean()[-1]
        largeSMA_list = []
        smallSMA_list = []

        for x in range(largeSMASize,len(bars)):
            largeSMA_list.append(bars.close.rolling(largeSMASize).mean()[x])

        for x in range(smallSMASize,len(bars)):
            smallSMA_list.append(bars.close.rolling(smallSMASize).mean()[x])

        if smallSMA > largeSMA:
            try:
                api.get_position(symbol)

            except(APIError):
                api.submit_order(
                    symbol=symbol,
                    qty=str(QUANTITY),
                    )
                print(f"BOT {QUANTITY} {symbol}")

        else:
            try:
                position = api.get_position(symbol)
                api.submit_order(
                    symbol=symbol,
                    type="market",
                    side="sell",
                    qty=position.qty
                )
                print(f"SOLD {position.qty} {symbol}")
            except(APIError):
                pass

    with sql.connect("botData.db") as con:
        cur = con.cursor()
        cur.execute('DELETE FROM Analysis')  ##delete old values

        for x in range(largeSMASize, len(bars.volume)):
            cur.execute("INSERT INTO SMAAnalysis(Symbol,Date,LargeSMA,SmallSMA) VALUES (?,?,?,?)",
                        (symbol, (bars.index[x].to_pydatetime()).date(), float(bars.close.rolling(smallSMASize).mean()[x]), float(bars.close.rolling(smallSMASize).mean()[x])),)  # update with new values



def volumePrice(symbols, timeFrame):
    print(f"Running Volume on {symbols} with size {timeFrame}")
    if account.status != "ACTIVE":
        logging.error("Alpaca Account is not able to trade")
        return False
    symbolsToTrade = symbols

    currentDate = datetime.today().date() - timedelta(days=1)
    startDate = currentDate - timedelta(days=timeFrame)

    for symbol in symbolsToTrade:
        bars = api.get_bars(symbol, TimeFrame.Day, start=startDate, end=currentDate, limit=timeFrame).df

        avgVol = bars.volume.mean()  # gets average volume last specified days (timeFrame)
        currentVol = bars.volume[-1]
        priceChange = bars.close[-1] - bars.close[-6]  # gets price change last 5 days
        if(currentVol > avgVol and priceChange > 0):

            print("currentVol > avgVol and price is up")
            try:
                api.get_position(symbol)

            except(APIError):
                # print("There is no current position. (BUY!)")

                api.submit_order(
                    symbol=symbol,
                    side='buy',
                    type='market',
                    qty=str(QUANTITY),
                    time_in_force='day',
                    order_class='trailing_stop',
                    trail_percent='5',
                    )
                print(f"BOT {QUANTITY} {symbol}")

        else:
            pass
            #print("avgVol > currentVol or price is down")

        with sql.connect("botData.db") as con:
            cur = con.cursor()
            cur.execute('DELETE FROM Analysis')

            for x in range(0, len(bars.volume)):
                cur.execute("REPLACE INTO Analysis(Symbol, Date, Price) VALUES (?,?,?)",
                            (symbol, (bars.index[x].to_pydatetime()).date(), float(bars.volume[x])))  # update with new values



def runEMA(symbols, timeSpan):
    print(f"Running EMA on {symbols} with size {timeSpan}")
    if account.status != "ACTIVE":
        logging.error("Alpaca Account is not able to trade")
        return False

    symbolsToTrade = symbols

    currentDate = datetime.today().date() - timedelta(days=1)
    startDate = currentDate - timedelta(days=timeSpan)

    for symbol in symbolsToTrade:
        bars = api.get_bars(symbol, TimeFrame.Day, start=startDate, end=currentDate).df
        length = len(bars)  # gets amount of open days in time frame

        todaysPrice = bars.close[length - 1]
        yesterdaysPrice = bars.close[length - 2]

        priceList = []

        for x in range(0, length):
            priceList.append(float(bars.close[x]))

        emaOfPrice = emaCalculation(priceList, length)  # store ema prices inside of a list

        if float(todaysPrice) > float(emaOfPrice[length - 1]) and float(yesterdaysPrice) > float(emaOfPrice[length - 2]):
            try:
                api.get_position(symbol)
            except:
                api.submit_order(
                    symbol=symbol,
                    side='buy',
                    type='market',
                    qty=str(QUANTITY),
                    time_in_force='day',
                    )
                print(f"BOT {QUANTITY} {symbol}")

        elif float(todaysPrice) < float(emaOfPrice[length - 1]) and float(yesterdaysPrice) < float(emaOfPrice[length - 2]):
            try:
                position = api.get_position(symbol)
                api.submit_order(
                    symbol=symbol,
                    qty=position.qty
                    )
                print(f"SOLD {QUANTITY} {symbol}")
            except(APIError):
                pass
        else:
            pass

        with sql.connect("botData.db") as con:
            cur = con.cursor()
            cur.execute('DELETE FROM Analysis')             ##delete old values

            for x in range(0, len(emaOfPrice)):
                cur.execute("REPLACE INTO Analysis(Symbol, Date, Price) VALUES (?,?,?)",
                            (symbol, (bars.index[x].to_pydatetime()).date(), emaOfPrice[x]))  #update with new values


def emaCalculation(price_list, days):
    ema = [sum(price_list) / days]  # first obersvation is the sma of the closing prices

    for price in price_list[1:]:  # perform EMA calculation using prices
        ema.append((price * (2 / (1 + days))) + ema[-1] * (1 - (2 / (1 + days))))
        final_ema = my_formatted_list = ['%.2f' % x for x in ema]

    return final_ema

def setQuantity(qt):
    global QUANTITY
    QUANTITY = qt
    print(f"New Quantity: {QUANTITY}")

def addSymbol(symbol):
    try:
        asset = api.get_asset(symbol)
        if not asset.tradable:
            print(f"ERROR: {symbol} is not tradeable on Alpaca")
        else:
            global SYMBOLS
            SYMBOLS.append(symbol)
            print(f"Added {symbol} to list of symbols")

    except(APIError):
        print(f"ERROR: {symbol} is invalid")


def getCurrentBalance():
    account = api.get_account()
    return account.portfolio_value

def getPortfolioHistory():
    return api.get_portfolio_history()
