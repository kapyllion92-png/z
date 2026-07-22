class PremiumDiscountEngine:

    def analyze(self, candles):

        result = {
            "premium": False,
            "discount": False,
            "equilibrium": False,
            "zone": None,
            "score": 0,
            "reasons": []
        }


        if len(candles) < 20:
            return result


        highs = [
            c["high"] for c in candles[-20:]
        ]

        lows = [
            c["low"] for c in candles[-20:]
        ]


        high = max(highs)
        low = min(lows)


        equilibrium = (
            high + low
        ) / 2


        price = candles[-1]["close"]


        # Premium zone

        if price > equilibrium:

            result["premium"] = True
            result["zone"] = "PREMIUM"

            result["score"] += 10

            result["reasons"].append(
                "PREMIUM ZONE"
            )


        # Discount zone

        if price < equilibrium:

            result["discount"] = True
            result["zone"] = "DISCOUNT"

            result["score"] += 10

            result["reasons"].append(
                "DISCOUNT ZONE"
            )


        # Equilibrium

        if abs(price - equilibrium) / price < 0.002:

            result["equilibrium"] = True
            result["zone"] = "EQUILIBRIUM"

            result["score"] += 5

            result["reasons"].append(
                "EQUILIBRIUM 50%"
            )


        result["score"] = min(
            result["score"],
            100
        )


        return result
