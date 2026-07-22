from app.exchange.bybit_client import BybitClient
from app.storage.data_storage import DataStorage
import time


class HistoryCollector:


    def __init__(self):

        self.bybit = BybitClient()

        self.storage = DataStorage()


        self.timeframes = [

            "5",
            "15",
            "60",
            "240",
            "D"

        ]



    def collect(self):


        symbols = self.bybit.get_symbols()


        print(
            "MONETS:",
            len(symbols)
        )


        for symbol in symbols:


            print(
                "LOAD:",
                symbol
            )


            for tf in self.timeframes:


                try:


                    candles = self.bybit.get_candles(

                        symbol,

                        tf,

                        1000

                    )


                    self.storage.save_candles(

                        symbol,

                        tf,

                        candles

                    )


                    print(

                        symbol,
                        tf,
                        len(candles)

                    )


                except Exception as e:


                    print(

                        "ERROR",
                        symbol,
                        tf,
                        e

                    )


                time.sleep(0.2)



if __name__=="__main__":


    collector=HistoryCollector()

    collector.collect()
