import json, requests
from config import *

BASE_URL = "https://paper-api.alpaca.markets"
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRETE_KEY}
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)


def get_account():
    r = requests.get(ACCOUNT_URL, headers = HEADERS)
    return json.load(r.cont)


def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDERS_URL,json=data, headers = HEADERS)

    return json.loads(r.content)

