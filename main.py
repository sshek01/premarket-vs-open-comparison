import requests
import yfinance as yf
from datetime import datetime, timezone

hype_url = "https://api.hyperliquid.xyz/info"

#Set absolute times
startTime = datetime(2026, 8, 11, 0, 0, 0, tzinfo=timezone.utc)
endTime = datetime(2026, 9, 11, 23, 59, 59, tzinfo=timezone.utc)

exactStart = int(startTime.timestamp() * 1000)
exactEnd = int(endTime.timestamp() * 1000)

#JSON payload, candlesticks 15 min interval
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
    
    #Grab specific candles before market open, compute mid price
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

aaplMids= price_info("xyz:AAPL", exactStart, exactEnd)


#START YFINANCE 
priceList = []
datesList = []

aapl = yf.Ticker("AAPL")

#Grab Dates and Open Prices
data = aapl.history(start = "2026-8-10", end = "2026-9-12")
dates = data.index.strftime('%m-%d').tolist()
openPrice = data['Open'].tolist()

for i in openPrice:
    priceList.append(float(f"{i:.2f}"))

#Calculate price discrepency
priceGap = []

for i in range(24):
    gap = ((priceList[i] - aaplMids[i]) / aaplMids[i]) * 100
    priceGap.append(f"{gap:.2f}")







