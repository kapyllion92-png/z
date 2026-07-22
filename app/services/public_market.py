import requests


class PublicMarketData:


    def __init__(self):

        self.url = "https://api.bybit.com"


    def get_candles(
        self,
        symbol="BTCUSDT",
        interval="60",
        limit=100
    ):

        response = requests.get(
            self.url + "/v5/market/kline",
            params={
                "category":"linear",
                "symbol":symbol,
                "interval":interval,
                "limit":limit
            },
            timeout=10
        )


        data = response.json()


        candles = data["result"]["list"]


        result = []


        for c in candles[::-1]:

            result.append(
                {
                    "time": int(c[0]),
                    "open": float(c[1]),
                    "high": float(c[2]),
                    "low": float(c[3]),
                    "close": float(c[4]),
                    "volume": float(c[5])
                }
            )


        return result
