class Strategy:


    def analyze(self, features):


        close = features["close"]

        sma = features["sma"]

        rsi = features["rsi"]



        trend = "BULLISH" if close > sma else "BEARISH"



        if trend == "BULLISH" and rsi >= 45:

            signal = "LONG"


        elif trend == "BEARISH" and rsi <= 55:

            signal = "SHORT"


        else:

            signal = "NO_TRADE"



        momentum = "NEUTRAL"


        return {


            "trend":
                trend,


            "momentum":
                momentum,


            "signal":
                signal

        }
