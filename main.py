import requests
import yfinance as yf
from datetime import datetime, timezone

hype_url = "https://api.hyperliquid.xyz/info"

startTime = datetime(2026, 8, 11, 0, 0, 0, tzinfo=timezone.utc)
endTime = datetime(2026, 9, 11, 23, 59, 59, tzinfo=timezone.utc)

exactStart = int(startTime.timestamp() * 1000)
exactEnd = int(endTime.timestamp() * 1000)


def price_info(ticker, exactStart, exactEnd):
    payload = {
        "type" : "candleSnapshot",
        "req": {
            "coin": ticker,
            "interval": "15m",
            "startTime": exactStart,
            "endTime": exactEnd,
        },
    
    }

    response = requests.post(hype_url, json=payload)

    if response.status_code != 200:
        return []

    candles = response.json()
    hypeData = []

    for candle in candles:
        candleTime = datetime.fromtimestamp(
            candle["t"] / 1000, tz = timezone.utc
        )

        if candleTime.hour == 13 and candleTime.minute == 15 and candleTime.weekday() < 5:
            highPx = float(candle["h"])
            lowPx = float(candle["l"])
            mid = (highPx + lowPx) / 2
            hypeData.append(round(mid, 2))

    return hypeData

aaplMids = price_info("xyzAAPL", exactStart, exactEnd)
print(aaplMids)

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



    







