from app.services.bybit_client import BybitClient
from app.services.market_analyzer import MarketAnalyzer


SIGNALS = []


class ScannerEngine:


    def __init__(self):

        self.client = BybitClient()
        self.analyzer = MarketAnalyzer()


    def scan_symbol(self, symbol, interval):

        try:

            candles = self.client.get_candles(
                symbol,
                interval,
                200
            )


            if len(candles) < 50:
                return None


            result = self.analyzer.analyze(
                candles
            )


            ranking = result.get(
                "ranking",
                {}
            )


            signal = ranking.get(
                "signal",
                "WAIT"
            )


            if signal == "WAIT":
                return None



            features = result.get(
                "features",
                {}
            )


            return {

                "symbol": symbol,

                "timeframe": interval,

                "direction": signal,

                "score": ranking.get(
                    "score",
                    0
                ),

                "price": candles[-1]["close"],

                "rsi": features.get(
                    "rsi",
                    0
                ),

                "confidence": ranking.get(
                    "score",
                    0
                ),

                "stop": 0,

                "reasons": ranking.get(
                    "reasons",
                    []
                )

            }


        except Exception as e:

            print(
                "SCAN ERROR",
                symbol,
                interval,
                e
            )

            return None





def get_signals():


    global SIGNALS


    SIGNALS=[]


    client = BybitClient()

    engine = ScannerEngine()


    symbols = client.get_symbols()


    intervals = [
        "5",
        "15",
        "60",
        "240",
        "D"
    ]


    print(
        "ÌÎÍÅÒ:",
        len(symbols)
    )


    for symbol in symbols:


        for interval in intervals:


            result = engine.scan_symbol(
                symbol,
                interval
            )


            if result:

                SIGNALS.append(
                    result
                )



    SIGNALS.sort(
        key=lambda x:x["score"],
        reverse=True
    )


    print(
        "ÑÈÃÍÀËÎÂ:",
        len(SIGNALS)
    )


    return SIGNALS[:50]
