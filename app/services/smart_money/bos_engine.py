from typing import List, Dict


class BOSEngine:

    def __init__(self):
        self.name = "BOS ENGINE v1.0"


    def analyze(self, candles: List[Dict]):

        if len(candles) < 20:
            return {
                "engine": self.name,
                "status": "NOT ENOUGH DATA",
                "score": 0,
                "ready": False
            }


        highs = [
            c["high"]
            for c in candles
        ]

        lows = [
            c["low"]
            for c in candles
        ]


        last_close = candles[-1]["close"]


        previous_high = max(
            highs[-20:-5]
        )

        previous_low = min(
            lows[-20:-5]
        )


        bos = None
        score = 0
        reason = []


        if last_close > previous_high:

            bos = "BULLISH"

            score = 100

            reason.append(
                "BREAK ABOVE STRUCTURE"
            )


        elif last_close < previous_low:

            bos = "BEARISH"

            score = 100

            reason.append(
                "BREAK BELOW STRUCTURE"
            )


        else:

            bos = "NONE"

            score = 50

            reason.append(
                "STRUCTURE NOT BROKEN"
            )


        return {

            "engine": self.name,

            "bos": bos,

            "score": score,

            "ready": score >= 85,

            "previous_high": previous_high,

            "previous_low": previous_low,

            "current_price": last_close,

            "reasons": reason

        }
