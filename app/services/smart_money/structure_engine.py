class StructureEngine:

    def analyze(self, candles):

        result = {
            "swing_high": False,
            "swing_low": False,
            "higher_high": False,
            "higher_low": False,
            "lower_high": False,
            "lower_low": False,
            "bos": False,
            "choch": False,
            "trend": "NEUTRAL",
            "score": 0,
            "reasons": []
        }


        if len(candles) < 10:
            return result


        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]


        prev_high = highs[-3]
        last_high = highs[-1]

        prev_low = lows[-3]
        last_low = lows[-1]


        # Swing High

        if highs[-2] > highs[-3] and highs[-2] > highs[-1]:

            result["swing_high"] = True

            result["score"] += 5

            result["reasons"].append(
                "SWING HIGH"
            )


        # Swing Low

        if lows[-2] < lows[-3] and lows[-2] < lows[-1]:

            result["swing_low"] = True

            result["score"] += 5

            result["reasons"].append(
                "SWING LOW"
            )


        # Higher High

        if last_high > prev_high:

            result["higher_high"] = True

            result["trend"] = "BULLISH"

            result["score"] += 5

            result["reasons"].append(
                "HIGHER HIGH"
            )


        # Higher Low

        if last_low > prev_low:

            result["higher_low"] = True

            result["trend"] = "BULLISH"

            result["score"] += 5

            result["reasons"].append(
                "HIGHER LOW"
            )


        # Lower High

        if last_high < prev_high:

            result["lower_high"] = True

            result["trend"] = "BEARISH"

            result["score"] += 5

            result["reasons"].append(
                "LOWER HIGH"
            )


        # Lower Low

        if last_low < prev_low:

            result["lower_low"] = True

            result["trend"] = "BEARISH"

            result["score"] += 5

            result["reasons"].append(
                "LOWER LOW"
            )


        # BOS

        if result["higher_high"]:

            result["bos"] = True

            result["score"] += 10

            result["reasons"].append(
                "BULLISH BOS"
            )


        if result["lower_low"]:

            result["bos"] = True

            result["score"] += 10

            result["reasons"].append(
                "BEARISH BOS"
            )


        # CHoCH

        if (
            result["higher_low"]
            and
            result["lower_high"]
        ):

            result["choch"] = True

            result["score"] += 15

            result["reasons"].append(
                "MARKET STRUCTURE CHoCH"
            )


        result["score"] = min(
            result["score"],
            100
        )


        return result