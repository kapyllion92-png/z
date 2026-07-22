class SweepDetector:


    def analyze(
        self,
        candles,
        liquidity
    ):

        result = {

            "sweep": False,

            "type": None,

            "level": None,

        }


        if not candles:
            return result


        candle = candles[-1]


        high = candle[5]

        low = candle[6]

        close = candle[7]



        # BUY SIDE LIQUIDITY
        # Снятие равных максимумов

        for pool in liquidity.get(
            "equal_highs",
            []
        ):

            level = pool["price"]


            if (
                high > level
                and close < level
            ):

                return {

                    "sweep": True,

                    "type":
                        "BUY_SIDE_LIQUIDITY",

                    "level": level,

                }



        # SELL SIDE LIQUIDITY
        # Снятие равных минимумов

        for pool in liquidity.get(
            "equal_lows",
            []
        ):

            level = pool["price"]


            if (
                low < level
                and close > level
            ):

                return {

                    "sweep": True,

                    "type":
                        "SELL_SIDE_LIQUIDITY",

                    "level": level,

                }



        return result
