from pybit.unified_trading import HTTP


class BybitClient:

    def __init__(self):

        self.session = HTTP(
            testnet=False
        )


    def get_symbols(self):

        result = self.session.get_instruments_info(
            category="linear"
        )

        symbols=[]

        for item in result["result"]["list"]:

            if item["quoteCoin"]=="USDT":

                symbols.append(
                    item["symbol"]
                )

        return symbols



    def get_candles(
        self,
        symbol,
        interval,
        limit=1000
    ):

        result=self.session.get_kline(

            category="linear",

            symbol=symbol,

            interval=interval,

            limit=limit

        )


        candles=[]


        for c in result["result"]["list"]:

            candles.append({

                "time": int(c[0]),

                "open": float(c[1]),

                "high": float(c[2]),

                "low": float(c[3]),

                "close": float(c[4]),

                "volume": float(c[5])

            })


        return candles
