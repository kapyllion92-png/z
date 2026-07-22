from typing import Dict, List


class PremiumDiscountEngine:


    def analyze(self, candles: List[Dict]):

        result = {

            "premium": False,
            "discount": False,
            "equilibrium": False,

            "long_valid": False,
            "short_valid": False,

            "zone": None,

            "score": 0,
            "reasons": []

        }


        if len(candles) < 20:
            return result


        highs = [
            float(c["high"])
            for c in candles[-20:]
        ]

        lows = [
            float(c["low"])
            for c in candles[-20:]
        ]


        closes = [
            float(c["close"])
            for c in candles[-20:]
        ]


        high = max(highs)
        low = min(lows)

        close = closes[-1]


        equilibrium = (
            high + low
        ) / 2


        # =====================
        # PREMIUM
        # =====================

        if close > equilibrium:

            result["premium"] = True
            result["zone"] = "PREMIUM"

            result["score"] += 10

            result["reasons"].append(
                "PREMIUM ZONE"
            )


        # =====================
        # DISCOUNT
        # =====================

        if close < equilibrium:

            result["discount"] = True
            result["zone"] = "DISCOUNT"

            result["score"] += 10

            result["reasons"].append(
                "DISCOUNT ZONE"
            )


        # =====================
        # EQUILIBRIUM
        # =====================

        if abs(close-equilibrium) / equilibrium < 0.002:

            result["equilibrium"] = True
            result["zone"] = "EQUILIBRIUM"

            result["reasons"].append(
                "EQUILIBRIUM"
            )


        # =====================
        # DIRECTION VALIDATION
        # =====================

        if result["discount"]:

            result["long_valid"] = True

            result["score"] += 5

            result["reasons"].append(
                "LONG LOCATION VALID"
            )


        if result["premium"]:

            result["short_valid"] = True

            result["score"] += 5

            result["reasons"].append(
                "SHORT LOCATION VALID"
            )


        return result
