class FVGEngine:

    def analyze(self, candles):

        result = {
            "fair_value_gap": False,
            "bullish_fvg": False,
            "bearish_fvg": False,
            "imbalance": False,
            "filled": False,
            "score": 0,
            "reasons": []
        }


        if len(candles) < 3:
            return result


        c1 = candles[-3]
        c2 = candles[-2]
        c3 = candles[-1]


        # Bullish Fair Value Gap

        if c1["high"] < c3["low"]:

            result["fair_value_gap"] = True
            result["bullish_fvg"] = True
            result["imbalance"] = True

            result["score"] += 15

            result["reasons"].append(
                "BULLISH FAIR VALUE GAP"
            )


        # Bearish Fair Value Gap

        if c1["low"] > c3["high"]:

            result["fair_value_gap"] = True
            result["bearish_fvg"] = True
            result["imbalance"] = True

            result["score"] += 15

            result["reasons"].append(
                "BEARISH FAIR VALUE GAP"
            )


        # FVG Mitigation

        if result["fair_value_gap"]:

            gap_high = max(
                c1["high"],
                c3["high"]
            )

            gap_low = min(
                c1["low"],
                c3["low"]
            )


            price = c3["close"]


            if gap_low <= price <= gap_high:

                result["filled"] = True

                result["score"] += 5

                result["reasons"].append(
                    "FVG MITIGATION"
                )


        result["score"] = min(
            result["score"],
            100
        )


        return result