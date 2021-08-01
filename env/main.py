from requests.api import get
import websocket
import asyncio
import time
import json
import sqlite3
from get_price import get_curr_price
from work_with_db import create_connection, create_table
# --------------------------------------------------
# GAP info
with open('../config.json') as f :
    file = json.load(f)
    GAP = file['robot']['gap']
    GAP_IGNORE = file['robot']['gap_ignore']

DB_FILE = r'pythonsqlite.db'



sell_price_list = []
buy_price_list = []
# Get current price
curr_price = get_curr_price()
buy_price = float(curr_price - GAP/2)


def buy_order(price):
    """
    We should check that if we our price equal our 'target' price, which we computed above
    :return: Bool, True  if "target" price == current price, else False 
    """
    if buy_price == float(price):
        buy_price_list.append(price)
        return True
    else:
        pass


def get_user_price():
    pr = int(input('Please type price, where you want to buy, current price is:',curr_price))
    return pr


def insert_to_database(coin:str, price, order:str):
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()
    insert_in_table = cursor.execute("INSERT INTO bot VALUES (\
        {order},{coin}, {price}, {GAP})")
    conn.close()
    print('We added one price')    


def buy_or_sell(price):
    """
    It's like "checkpointer" which select "buy" or "sell"
    """
    if len(buy_price_list) > len(sell_price_list):
         # because if len(buy_price_list) > len(sell_price_list) that's mean that we buy and now we should sell order
        sell_order(price)
        order_to_sell = 'sell'
        return order_to_sell

    elif len(buy_price_list) == len(sell_price_list):# if it's equal than we call buy_order
        buy_order(price)
        order_to_buy = 'buy'
        return order_to_buy
    else:
        buy_order(price)
        order_to_buy = 'buy'
        return order_to_buy


def sell_order(price):
    if buy_price_list is not None:
        last_price = buy_price_list[::-1][0] # get last price, when we buy and add it GAP/2
        sell_price = float(last_price + GAP/2)
        sell_price_list.add(sell_price)

        # return float(last_price)


def on_message(ws, message):
    kline = json.loads(message) # convert our message to json and load it
    close_price = kline['k']['c']  # fetching our price 
    close_price_int = "".join(close_price)
    close_price_int = map(round(1),int(close_price_int) )
    print('Close-->',close_price)
    buy_order(close_price)
    order = buy_or_sell(close_price)
    insert_to_database(coin, close_price_int,order)


def main():
    coin = 'btcusdt'
    interval = '1m'
    socket = f'wss://stream.binance.com:9443/ws/{coin}@kline_{interval}'
    ws = websocket.WebSocketApp(socket, on_message=on_message)
    ws.run_forever()

main()
