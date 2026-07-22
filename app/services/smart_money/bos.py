class BOSEngine:


    def analyze(
        self,
        candles,
        pivot_highs,
        pivot_lows,
    ):

        result = {
            "trend_structure": "RANGE",
            "bos": False,
            "choch": False,
            "break_level": None,
        }


        if not candles:
            return result


        close = candles[-1][7]


        last_high = None
        last_low = None


        if pivot_highs:
            last_high = pivot_highs[-1]


        if pivot_lows:
            last_low = pivot_lows[-1]



        if last_high and close > last_high["price"]:

            result["trend_structure"] = "BULLISH"
            result["bos"] = True

            result["break_level"] = {
                "type": "HIGH",
                "price": last_high["price"],
            }



        elif last_low and close < last_low["price"]:

            result["trend_structure"] = "BEARISH"
            result["bos"] = True

            result["break_level"] = {
                "type": "LOW",
                "price": last_low["price"],
            }


        return result
