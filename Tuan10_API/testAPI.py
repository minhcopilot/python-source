import requests
import pandas as pd
API_KEY='2113ca0db38065eff218b14f2a00cccdf9e191f41b50f4cbef8788d352f56f67'
ROOT_API='https://min-api.cryptocompare.com/data/'
# def get_price(symbol,list_currency):
#     join_currency= ','.join(list_currency)
#     url =f'{ROOT_API}price?fsym={symbol}&tsyms={join_currency}&api_key={API_KEY}'
#     data = requests.get(url).json()
#     return data

# print(get_price('ETH',['USD','EUR','JPY']))


def get_history(symbol,currency,limit):
    url =f'{ROOT_API}histoday?fsym={symbol}&tsym={currency}&limit={limit}&api_key={API_KEY}'
    data = requests.get(url).json()
    data_csv=pd.read_json(data)
    return data_csv

print(get_history('ETH','USD',10))