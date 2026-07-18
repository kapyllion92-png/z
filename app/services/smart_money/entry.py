class EntryEngine:


    def analyze(
        self,
        features,
        strategy,
        structure
    ):

        result = {

            "setup": "NONE",

            "confidence": 0,

            "entry_zone": None,

            "stop_loss": None,

            "take_profit": None,

            "risk_reward": None,

        }


        signal = strategy.get(
            "signal"
        )


        atr = features.get(
            "atr"
        )


        if not atr:
            return result



        #
        # LONG
        #

        if signal == "LONG":


            blocks = structure.get(
                "bullish_order_blocks",
                []
            )


            if blocks:


                block = blocks[-1]


                entry_low = block["low"]

                entry_high = block["high"]


                stop = entry_low - atr * 0.5



                highs = structure.get(
                    "equal_highs",
                    []
                )


                if highs:


                    target = highs[-1]["price"]


                    risk = entry_high - stop

                    reward = target - entry_high



                    if risk > 0:


                        rr = reward / risk



                        result = {

                            "setup":
                                "LONG",


                            "confidence":
                                70,


                            "entry_zone":
                            {

                                "low":
                                    entry_low,

                                "high":
                                    entry_high,

                            },


                            "stop_loss":
                                round(
                                    stop,
                                    2
                                ),


                            "take_profit":
                                round(
                                    target,
                                    2
                                ),


                            "risk_reward":
                                round(
                                    rr,
                                    2
                                ),

                        }



        #
        # SHORT
        #

        elif signal == "SHORT":


            blocks = structure.get(
                "bearish_order_blocks",
                []
            )


            if blocks:


                block = blocks[-1]


                entry_low = block["low"]

                entry_high = block["high"]


                stop = entry_high + atr * 0.5



                lows = structure.get(
                    "equal_lows",
                    []
                )


                target = None


                if lows:

                    target = lows[-1]["price"]



                result = {


                    "setup":
                        "SHORT",


                    "confidence":
                        70,


                    "entry_zone":
                    {

                        "low":
                            entry_low,

                        "high":
                            entry_high,

                    },


                    "stop_loss":
                        round(
                            stop,
                            2
                        ),


                    "take_profit":
                        target,


                }



        return result
