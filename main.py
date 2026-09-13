import requests
import yfinance as yf
import datetime

hype_url = "https://api.hyperliquid.xyz/info"

startTime = datetime.datetime(2026, 8, 11, 0, 0, 0, tzinfo=datetime.timezone.utc)
endTime = datetime.datetime(2026, 9, 11, 23, 59, 59, tzinfo=datetime.timezone.utc)


def price_info(ticker):
    payload = {
        "type" : "candleSnapshot",
    
    }

    response = requests.post(hype_url, json=payload)

    if response.status_code == 200:
        hype_data = response.json()
        dict_parse = hype_data.get(ticker)
        return dict_parse
    else:
        return None

price = price_info("BTC")
print (price)

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



    







