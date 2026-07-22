class LiquidityEngine:


    def find_equal_highs(
        self,
        pivot_highs,
        tolerance=0.002
    ):

        pools = []

        for i in range(len(pivot_highs)):

            for j in range(i + 1, len(pivot_highs)):

                price1 = pivot_highs[i]["price"]
                price2 = pivot_highs[j]["price"]

                difference = abs(price1 - price2) / price1

                if difference <= tolerance:

                    pools.append({

                        "type": "EQUAL_HIGH",

                        "side": "BUY_SIDE_LIQUIDITY",

                        "price": round(
                            (price1 + price2) / 2,
                            2
                        ),

                        "points": [
                            pivot_highs[i],
                            pivot_highs[j]
                        ]

                    })

        return pools



    def find_equal_lows(
        self,
        pivot_lows,
        tolerance=0.002
    ):

        pools = []

        for i in range(len(pivot_lows)):

            for j in range(i + 1, len(pivot_lows)):

                price1 = pivot_lows[i]["price"]
                price2 = pivot_lows[j]["price"]

                difference = abs(price1 - price2) / price1

                if difference <= tolerance:

                    pools.append({

                        "type": "EQUAL_LOW",

                        "side": "SELL_SIDE_LIQUIDITY",

                        "price": round(
                            (price1 + price2) / 2,
                            2
                        ),

                        "points": [
                            pivot_lows[i],
                            pivot_lows[j]
                        ]

                    })

        return pools



    def detect_liquidity_grab(
        self,
        candles,
        pools
    ):

        result = []

        if not candles:
            return result


        candle = candles[-1]


        for pool in pools:

            level = pool["price"]


            # снятие верхней ликвидности

            if (
                pool["side"] == "BUY_SIDE_LIQUIDITY"
                and candle["high"] > level
                and candle["close"] < level
            ):

                result.append({

                    "type": "LIQUIDITY_GRAB",

                    "direction": "SHORT",

                    "level": level,

                    "reason":
                    "Stop Run above Equal High"

                })



            # снятие нижней ликвидности

            if (
                pool["side"] == "SELL_SIDE_LIQUIDITY"
                and candle["low"] < level
                and candle["close"] > level
            ):

                result.append({

                    "type": "LIQUIDITY_GRAB",

                    "direction": "LONG",

                    "level": level,

                    "reason":
                    "Stop Run below Equal Low"

                })


        return result



    def detect_return_after_sweep(
        self,
        candles,
        grabs
    ):

        result = []


        if not candles:
            return result


        price = candles[-1]["close"]


        for grab in grabs:


            distance = abs(
                price - grab["level"]
            ) / grab["level"]


            if distance <= 0.003:


                result.append({

                    "type":
                    "RETURN_AFTER_SWEEP",

                    "direction":
                    grab["direction"],

                    "level":
                    grab["level"],

                    "confirmation":
                    True

                })


        return result



    def analyze(
        self,
        pivot_highs,
        pivot_lows,
        candles=None
    ):


        equal_highs = self.find_equal_highs(
            pivot_highs
        )


        equal_lows = self.find_equal_lows(
            pivot_lows
        )


        pools = (
            equal_highs
            +
            equal_lows
        )


        grabs = []

        returns = []


        if candles:


            grabs = self.detect_liquidity_grab(
                candles,
                pools
            )


            returns = self.detect_return_after_sweep(
                candles,
                grabs
            )


        return {


            "liquidity_pools":
            pools,


            "equal_highs":
            equal_highs,


            "equal_lows":
            equal_lows,


            "liquidity_grab":
            grabs,


            "return_after_sweep":
            returns,


            "liquidity_score":
            min(
                100,
                len(pools)*20
                +
                len(grabs)*30
            )

        }
    def liquidity_grab(self, candles):

        if len(candles) < 5:
            return False

        try:
            prev = candles[-2]
            last = candles[-1]

            return (
                float(last["low"]) < float(prev["low"])
                and
                float(last["close"]) > float(prev["low"])
            ) or (
                float(last["high"]) > float(prev["high"])
                and
                float(last["close"]) < float(prev["high"])
            )

        except Exception:
            return False



    def stop_run(self, candles):

        if len(candles) < 10:
            return False

        try:

            highs = [
                float(x["high"])
                for x in candles[-10:]
            ]

            lows = [
                float(x["low"])
                for x in candles[-10:]
            ]

            last = candles[-1]

            return (
                float(last["high"]) > max(highs[:-1])
                and
                float(last["close"]) < max(highs[:-1])
            ) or (
                float(last["low"]) < min(lows[:-1])
                and
                float(last["close"]) > min(lows[:-1])
            )

        except Exception:
            return False



    def stop_clusters(self, candles, tolerance=0.002):

        pools = []

        try:

            highs=[
                float(x["high"])
                for x in candles[-10:]
            ]

            lows=[
                float(x["low"])
                for x in candles[-10:]
            ]


            for i in range(len(highs)-1):

                if abs(highs[i]-highs[i+1]) / highs[i] <= tolerance:

                    pools.append(
                        {
                            "type":"BUY_SIDE_STOP_POOL",
                            "price":round(
                                (highs[i]+highs[i+1])/2,
                                2
                            )
                        }
                    )


                if abs(lows[i]-lows[i+1]) / lows[i] <= tolerance:

                    pools.append(
                        {
                            "type":"SELL_SIDE_STOP_POOL",
                            "price":round(
                                (lows[i]+lows[i+1])/2,
                                2
                            )
                        }
                    )


            return pools


        except Exception:

            return []


    def liquidity_return(self, candles):

        if len(candles) < 6:
            return False

        try:

            sweep = candles[-2]
            current = candles[-1]


            sweep_high = float(sweep["high"])
            sweep_low = float(sweep["low"])

            current_close = float(current["close"])


            return (
                current_close < sweep_high
                and
                current_close > sweep_low
            )


        except Exception:

            return False

