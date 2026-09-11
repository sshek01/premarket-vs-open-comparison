import requests

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
print(price)





