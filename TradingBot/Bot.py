from datetime import datetime, timedelta
import alpaca_trade_api as alpacaAPI
from alpaca_trade_api.rest import APIError, TimeFrame
from TradingBot.config import *
import logging
import sqlite3 as sql

BASE_URL = "https://paper-api.alpaca.markets"

api = alpacaAPI.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
account = api.get_account()
QUANTITY = 5


def runSMA(symbols, smallSMASize, largeSMASize):
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
        print(api.list_positions())

        if smallSMA > largeSMA:
            print("smallSMA > largeSMA")
            try:
                api.get_position(symbol)

            except(APIError):
                print("There is no current postion. (BUY!)")
                # api.submit_order(symbol, )

        else:
            print("LargeSMA > smallSMA")


def volumePrice(symbols, timeFrame):
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
        print(api.list_positions())
        print(
            "Ticker: {} \nTime Frame: {}\nAvg Vol: {} \nPrice Change last 5 Days: {} \nTime Frame: {} to {}".format(
                symbol, timeFrame, avgVol, priceChange, startDate, currentDate))  # testing can delete
        if (currentVol > avgVol and priceChange > 0):

            print("currentVol > avgVol and price is up")
            try:
                api.get_position(symbol)

            except(APIError):
                print("There is no current position. (BUY!)")

                api.submit_order(
                    symbol=symbol,
                    side='buy',
                    type='market',
                    qty=str(QUANTITY),
                    time_in_force='day',
                    order_class='trailing_stop',
                    trail_percent='5',
                    )

        else:
            print("avgVol > currentVol or price is down")


def runEMA(symbols, timeSpan):
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

        if float(todaysPrice) > float(emaOfPrice[length - 1]) and float(yesterdaysPrice) > float(
                emaOfPrice[length - 2]):
            api.submit_order(symbol, 5)
        elif float(todaysPrice) < float(emaOfPrice[length - 1]) and float(yesterdaysPrice) < float(
                emaOfPrice[length - 2]):
            api.submit_order(symbol, 5, "sell")
        else:
            pass

        with sql.connect("botData.db") as con:
            cur = con.cursor()
            for x in range(0, len(emaOfPrice)):
                cur.execute("INSERT INTO Analysis(Symbol, Date, Price) VALUES (?,?,?)",
                            (symbol, (bars.index[x].to_pydatetime()).date(), emaOfPrice[x]))

        print(cur.execute('SELECT * FROM Analysis').fetchall())


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
