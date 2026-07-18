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

                        "price": round(
                            (price1 + price2) / 2,
                            2
                        ),

                        "points": [
                            pivot_highs[i],
                            pivot_highs[j],
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

                        "price": round(
                            (price1 + price2) / 2,
                            2
                        ),

                        "points": [
                            pivot_lows[i],
                            pivot_lows[j],
                        ]

                    })


        return pools



    def analyze(
        self,
        pivot_highs,
        pivot_lows
    ):

        equal_highs = self.find_equal_highs(
            pivot_highs
        )


        equal_lows = self.find_equal_lows(
            pivot_lows
        )


        return {

            "equal_highs": equal_highs,

            "equal_lows": equal_lows,

            "liquidity_count":
                len(equal_highs)
                +
                len(equal_lows)

        }
