from datetime import datetime, timedelta
import alpaca_trade_api as alpacaAPI
from alpaca_trade_api.rest import APIError, TimeFrame
from TradingBot.config import *
import logging

BASE_URL = "https://paper-api.alpaca.markets"

api = alpacaAPI.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
account = api.get_account()

def runSMA(symbols, smallSMASize, largeSMASize):
    if account.status != "ACTIVE":
        logging.error("Alpaca Account is not able to trade")
        return False

    symbolsToTrade = symbols

    currentDate = datetime.today().date() - timedelta(days=1) # Since we are going to use close data, use the previous days close
    startDate = currentDate - timedelta(days=100)

    for symbol in symbolsToTrade:
        bars = api.get_bars(symbol, TimeFrame.Day,start=startDate, end= currentDate, limit=100).df

        largeSMA = bars.close.rolling(largeSMASize).mean()[-1]
        smallSMA = bars.close.rolling(smallSMASize).mean()[-1]
        print(api.list_positions())

        if smallSMA > largeSMA:
            print("smallSMA > largeSMA")
            try:
                api.get_position(symbol)

            except(APIError):
                print("There is no current postion. (BUY!)")
                #api.submit_order(symbol, )

        else:
            print("LargeSMA > smallSMA")

<<<<<<< HEAD
def volumePrice(symbols, volumeSize):
    if account.status != "ACTIVE":
        logging.error("Alpaca Account is not able to trade")
        return False
=======
    def runSomeOtherStrat(symbols):
        pass




        
        










>>>>>>> 283b6d938dc492346dd74eddde903de9141393a1

    symbolsToTrade = symbols

    currentDate = datetime.today().date() - timedelta(days=1)
    startDate = currentDate - timedelta(days=100)


    for symbol in symbolsToTrade:
        bars = api.get_bars(symbol, TimeFrame.Day, start=startDate, end=currentDate, limit=100).df

        avgVol = bars.volume.mean()
        currentVol = bars.volume[-1]
        priceChange = bars.close[-1] - bars.close[-6]
        print(api.list_positions())
        print("Ticker: {} \nAvg Vol: {} \nPrice Change last 5 Days: {} \nTime Frame: {} to {}".format(symbol, avgVol, priceChange, startDate, currentDate)) # testing can delete
        if(currentVol > avgVol and priceChange > 0):

            print("currentVol > avgVol and price is up")
            try:
                api.get_position(symbol)

            except(APIError):
                print("There is no current position. (BUY!)")
                #api.submit_order(symbol, )
                # need to push trade to database

        else:
            print("avgVol > currentVol or price is down")
