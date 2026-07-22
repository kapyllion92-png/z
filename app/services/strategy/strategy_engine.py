
class StrategyEngine:

    def analyze(self, candles):

        if not candles:
            return {
                "signal": "NO_DATA",
                "score": 0
            }

        closes = [
            float(c[4])
            for c in candles
        ]

        first = closes[-1]
        last = closes[0]

        change = ((first - last) / last) * 100

        signal = "SIDEWAYS"

        if change > 1:
            signal = "BULLISH"

        elif change < -1:
            signal = "BEARISH"


        return {
            "signal": signal,
            "change_percent": round(change, 3),
            "candles": len(candles)
        }
