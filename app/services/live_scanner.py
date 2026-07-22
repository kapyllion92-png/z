from app.services.scanner_engine import ScannerEngine
from app.services.bybit_client import BybitClient


class LiveScanner:


    def __init__(self):

        self.engine = ScannerEngine()
        self.client = BybitClient()



    def scan(self):

        signals = []


        try:

            symbols = self.client.get_symbols()

            print("=== LIVE РАДАР ===")
            print("Монет:", len(symbols))


            for symbol in symbols[:100]:

                try:

                    candles = self.client.get_candles(symbol)


                    print(
                        symbol,
                        "свечи:",
                        len(candles)
                    )


                    result = self.engine.scan_symbol(
                        symbol,
                        candles
                    )


                    print(
                        "RESULT:",
                        result
                    )


                    if result:

                        if isinstance(result, list):

                            signals.extend(result)

                        else:

                            signals.append(result)


                except Exception as e:

                    print(
                        "Ошибка монеты:",
                        symbol,
                        e
                    )



            print(
                "ИТОГО:",
                len(signals)
            )


            signals = sorted(
                signals,
                key=lambda x:x.get("сила",0),
                reverse=True
            )


            return {

                "статус":"LIVE",

                "время":"онлайн",

                "топ_предсигналов":
                signals[:10],

                "топ_сделок":
                signals[:10],

                "всего_сигналов":
                len(signals)

            }



        except Exception as e:


            print(
                "LIVE ERROR:",
                e
            )


            return {

                "статус":"ОШИБКА",

                "время":"онлайн",

                "топ_предсигналов":[],

                "топ_сделок":[],

                "всего_сигналов":0
            }
