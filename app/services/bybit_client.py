import requests


class BybitClient:


    BASE = "https://api.bybit.com"



    def get_symbols(self):

        url = self.BASE + "/v5/market/instruments-info"


        params = {
            "category": "linear"
        }


        r = requests.get(
            url,
            params=params,
            timeout=10
        )


        data = r.json()


        symbols = []


        for item in data["result"]["list"]:

            symbol = item.get(
                "symbol",
                ""
            )


            if symbol.endswith("USDT"):

                symbols.append(symbol)



        return symbols[:100]





    def get_candles(self, symbol, interval, limit=200):


        url = self.BASE + "/v5/market/kline"


        params = {

            "category": "linear",

            "symbol": symbol,

            "interval": interval,

            "limit": limit

        }


        r = requests.get(

            url,

            params=params,

            timeout=10

        )


        data = r.json()


        rows = data["result"]["list"]


        candles = []



        for c in reversed(rows):


            candles.append({

                "time": int(c[0]),

                "open": float(c[1]),

                "high": float(c[2]),

                "low": float(c[3]),

                "close": float(c[4]),

                "volume": float(c[5]),

                "turnover": float(c[6])

            })



        return candles