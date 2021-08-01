import requests
import json

with open('../config.json') as f :
    file = json.load(f)
    symbol = file['other_config']['symbols']


def get_curr_price():
    test = requests.get("https://api.binance.com/api/v1/ping")
    curr_price = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=%s" % symbol)
    curr_price = curr_price.json()
    curr_price = curr_price['price']
    return float(curr_price)


print("Current price BTC is -->", get_curr_price())