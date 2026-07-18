class CHoCHEngine:


    def analyze(
        self,
        candles,
        pivot_highs,
        pivot_lows,
    ):

        result = {
            "choch": False,
            "direction": None,
            "break_level": None,
        }


        if len(pivot_highs) < 2:
            return result


        if len(pivot_lows) < 2:
            return result


        close = candles[-1][7]


        last_high = pivot_highs[-1]
        previous_high = pivot_highs[-2]


        last_low = pivot_lows[-1]
        previous_low = pivot_lows[-2]



        # Bearish CHoCH
        # Price breaks previous higher low

        if (
            previous_low["price"] > last_low["price"]
            and close < last_low["price"]
        ):

            result["choch"] = True
            result["direction"] = "BEARISH"

            result["break_level"] = {
                "type": "LOW",
                "price": last_low["price"],
            }



        # Bullish CHoCH
        # Price breaks previous lower high

        elif (
            previous_high["price"] < last_high["price"]
            and close > last_high["price"]
        ):

            result["choch"] = True
            result["direction"] = "BULLISH"

            result["break_level"] = {
                "type": "HIGH",
                "price": last_high["price"],
            }



        return result
