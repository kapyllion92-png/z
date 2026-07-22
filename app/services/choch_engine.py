from dataclasses import dataclass


@dataclass
class Structure:
    swing_high: float = None
    swing_low: float = None


class CHoCHEngine:

    def __init__(self):
        self.engine = "CHoCH ENGINE v5.0"
        self.structure = Structure()


    def analyze(
        self,
        candles,
        volume_ratio=1,
        displacement=False
    ):

        result = {
            "engine": self.engine,
            "choch": "NONE",
            "bos": "NONE",
            "score": 0,
            "ready": False,
            "direction": None,
            "reasons": []
        }


        if len(candles) < 20:
            return result


        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]
        closes = [c["close"] for c in candles]


        current_high = max(highs[-5:])
        current_low = min(lows[-5:])


        previous_high = max(highs[-20:-5])
        previous_low = min(lows[-20:-5])


        close = closes[-1]


        score = 0


        # BULLISH BOS
        if close > previous_high:

            result["bos"] = "BULLISH"
            result["direction"] = "LONG"

            score += 20

            result["reasons"].append(
                "BULLISH BOS"
            )


        # BEARISH BOS
        elif close < previous_low:

            result["bos"] = "BEARISH"
            result["direction"] = "SHORT"

            score += 20

            result["reasons"].append(
                "BEARISH BOS"
            )


        # BULLISH CHoCH
        if (
            self.structure.swing_low
            and
            close > self.structure.swing_high
        ):

            result["choch"] = "BULLISH"

            result["direction"] = "LONG"

            score += 40

            result["reasons"].append(
                "BULLISH MARKET STRUCTURE SHIFT"
            )


        # BEARISH CHoCH
        elif (
            self.structure.swing_high
            and
            close < self.structure.swing_low
        ):

            result["choch"] = "BEARISH"

            result["direction"] = "SHORT"

            score += 40

            result["reasons"].append(
                "BEARISH MARKET STRUCTURE SHIFT"
            )


        self.structure.swing_high = current_high
        self.structure.swing_low = current_low


        if displacement:
            score += 20
            result["reasons"].append(
                "DISPLACEMENT"
            )


        if volume_ratio >= 1:
            score += 20
            result["reasons"].append(
                "VOLUME CONFIRMATION"
            )


        result["score"] = min(score,100)


        if score >= 70:
            result["ready"] = True


        return result
