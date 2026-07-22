import requests


class MarketFeed:


    def get_symbols(self):

        url = (
            "https://api.bybit.com/v5/market/tickers"
            "?category=linear"
        )

        data = requests.get(url).json()

        symbols = []

        for item in data["result"]["list"]:

            symbol = item["symbol"]

            if symbol.endswith("USDT"):

                symbols.append(symbol)


        return symbols[:100]



    def get_candles(
        self,
        symbol,
        interval="15",
        limit=200
    ):


        url = (

            "https://api.bybit.com/v5/market/kline"

            f"?category=linear"

            f"&symbol={symbol}"

            f"&interval={interval}"

            f"&limit={limit}"

        )


        data = requests.get(url).json()


        return data["result"]["list"]
