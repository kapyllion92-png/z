class TrendStrategy:


    def analyze(self, features):

        close = features["close"]
        ema = features["ema"]
        rsi = features["rsi"]


        result = {
            "trend": "NEUTRAL",
            "momentum": "NEUTRAL",
            "signal": "WAIT",
        }


        if close > ema:
            result["trend"] = "BULLISH"

        elif close < ema:
            result["trend"] = "BEARISH"



        if rsi >= 70:
            result["momentum"] = "OVERBOUGHT"

        elif rsi <= 30:
            result["momentum"] = "OVERSOLD"



        if (
            result["trend"] == "BULLISH"
            and result["momentum"] != "OVERBOUGHT"
        ):
            result["signal"] = "LONG"


        elif (
            result["trend"] == "BEARISH"
            and result["momentum"] != "OVERSOLD"
        ):
            result["signal"] = "SHORT"


        return result
