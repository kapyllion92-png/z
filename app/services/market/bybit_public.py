import requests


class BybitPublic:


    def __init__(self):

        self.url = "https://api.bybit.com/v5/market/kline"



    def get_candles(
        self,
        symbol="BTCUSDT",
        interval="60",
        limit=100
    ):


        params = {

            "category": "linear",

            "symbol": symbol,

            "interval": interval,

            "limit": limit

        }


        data = requests.get(
            self.url,
            params=params,
            timeout=10
        ).json()


        candles = []


        for item in data["result"]["list"]:


            candles.append([

                int(item[0]),      # time

                float(item[1]),    # open

                float(item[2]),    # high

                float(item[3]),    # low

                float(item[4]),    # close

                0,                 # placeholder

                0,                 # placeholder

                float(item[5])     # volume

            ])


        return candles[::-1]
