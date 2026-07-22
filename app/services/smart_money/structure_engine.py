from datetime import datetime


class StructureEngine:

    def __init__(self):
        self.name = "CHoCH ENGINE v4.0"


    def analyze(
        self,
        previous_high,
        previous_low,
        current_high,
        current_low,
        volume_ratio=1.0
    ):

        result = {
            "engine": self.name,
            "bos": False,
            "choch": False,
            "direction": "NONE",
            "score": 0,
            "ready": False,
            "reasons": []
        }


        # bullish BOS
        if current_high > previous_high:

            result["bos"] = True
            result["direction"] = "BULLISH"

            result["score"] += 25

            result["reasons"].append(
                "BULLISH BOS BREAK"
            )


        # bearish BOS
        elif current_low < previous_low:

            result["bos"] = True
            result["direction"] = "BEARISH"

            result["score"] += 25

            result["reasons"].append(
                "BEARISH BOS BREAK"
            )


        # bullish CHoCH
        if (
            current_low > previous_low
            and
            current_high > previous_high
        ):

            result["choch"] = True
            result["direction"] = "BULLISH"

            result["score"] += 30

            result["reasons"].append(
                "BULLISH MARKET STRUCTURE CHoCH"
            )


        # bearish CHoCH
        if (
            current_high < previous_high
            and
            current_low < previous_low
        ):

            result["choch"] = True
            result["direction"] = "BEARISH"

            result["score"] += 30

            result["reasons"].append(
                "BEARISH MARKET STRUCTURE CHoCH"
            )


        # volume confirmation

        if volume_ratio >= 1.2:

            result["score"] += 15

            result["reasons"].append(
                "VOLUME CONFIRMATION"
            )


        # displacement

        move = abs(current_high-current_low)

        if move > abs(previous_high-previous_low):

            result["score"] += 15

            result["reasons"].append(
                "DISPLACEMENT"
            )


        result["score"] = min(
            result["score"],
            100
        )


        if result["score"] >= 70:

            result["ready"] = True


        return result
