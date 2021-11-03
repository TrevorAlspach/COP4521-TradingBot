import json, requests
from TradingBot.config import *


BASE_URL = "https://paper-api.alpaca.markets"
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL)

def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.load(r.cont)

#Order Functions
def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        # "notional": notional,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)


def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)


def request_order(order_id):
    order_url = "{}/{}".format(ORDERS_URL, order_id)
    r = requests.get(order_url, headers=HEADERS)


def cancel_all_orders():
    r = requests.delete(ORDERS_URL, headers=HEADERS)


def cancel_order(order_id):
    order_url = "{}/{}".format(ORDERS_URL, order_id)
    r = requests.delete(order_url, headers=HEADERS)

#position functions
def get_all_open_positions():
    r = requests.get(POSITIONS_URL, headers=HEADERS)

    return json.load(r.cont)


def get_open_position(symbol):
    symbol_position_url = "{}/{}".format(POSITIONS_URL, symbol)
    r = requests.get(symbol_position_url, headers=HEADERS)

    return json.load(r.cont)

def close_all_positions():
    r = requests.delete(POSITIONS_URL, headers=HEADERS)

def close_position(symbol):
    symbol_position_url = "{}/{}".format(POSITIONS_URL, symbol)
    r = requests.delete(symbol_position_url, headers=HEADERS)

