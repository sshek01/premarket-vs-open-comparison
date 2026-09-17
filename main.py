import requests
import yfinance as yf
from datetime import datetime, timezone
import os
import mysql.connector
from dotenv import load_dotenv

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

ticker = "AAPL"

aapl = yf.Ticker("AAPL")

#Grab Dates and Open Prices
data = aapl.history(start = "2026-8-10", end = "2026-9-12")
dates = data.index.strftime('%Y-%m-%d').tolist()
openPrice = data['Open'].tolist()

for i in openPrice:
    priceList.append(float(f"{i:.2f}"))

#Calculate price discrepency
priceGap = []

for i in range(24):
    gap = ((priceList[i] - aaplMids[i]) / aaplMids[i]) * 100
    priceGap.append(f"{gap:.2f}")

#SQL connection

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", 3306))
)

cursor = connection.cursor()

data_to_insert = list(zip(dates, [ticker] * len(dates), priceList, aaplMids, priceGap))

insert_query = """
INSERT INTO self_project_data (dates, ticker, priceList, aaplMids, priceGap)
VALUES (%s, %s, %s, %s, %s)
"""

try:
    cursor.executemany(insert_query, data_to_insert)
    connection.commit()
    print(f"Successfully inserted {cursor.rowcount} rows into MySQL.")
except mysql.connector.Error as err:
    print(f"Database error: {err}")
    connection.rollback()
finally:
    cursor.close()
    connection.close()