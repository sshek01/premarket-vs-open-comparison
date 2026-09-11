import requests
import yfinance as yf

hype_url = "https://api.hyperliquid.xyz/info"

def price_info(ticker):

    response = requests.post(hype_url, json={"type" : "allMids"})

    if response.status_code == 200:
        hype_data = response.json()
        dict_parse = hype_data.get(ticker)
        return dict_parse
    else:
        return None

price = price_info("BTC")

#SPY,AAPL,SNDK
priceList = []
datesList = []

spy = yf.Ticker("SPY")

#Grab Dates and Open Prices
data = spy.history(period="1mo")

dates = data.index.strftime('%m-%d').tolist()
open_price = data['Open'].tolist()
for i in open_price:
    priceList.append(f"{i:.2f}")



    







