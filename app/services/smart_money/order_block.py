class OrderBlockDetector:


    def analyze(
        self,
        candles
    ):

        bullish_blocks = []

        bearish_blocks = []


        if len(candles) < 5:
            return {

                "bullish_order_blocks": [],

                "bearish_order_blocks": [],

            }



        for i in range(
            1,
            len(candles) - 2
        ):


            current = candles[i]

            next_candle = candles[i + 1]



            open_price = current[4]

            high = current[5]

            low = current[6]

            close = current[7]



            next_open = next_candle[4]

            next_close = next_candle[7]



            #
            # Bullish Order Block
            #
            # Красная свеча
            # затем сильный рост
            #

            if (
                close < open_price
                and next_close > next_open
                and next_close > high
            ):

                bullish_blocks.append({

                    "type":
                        "BULLISH_OB",

                    "high":
                        high,

                    "low":
                        low,

                    "index":
                        i,

                    "time":
                        current[3],

                })



            #
            # Bearish Order Block
            #
            # Зеленая свеча
            # затем сильное падение
            #

            if (
                close > open_price
                and next_close < next_open
                and next_close < low
            ):

                bearish_blocks.append({

                    "type":
                        "BEARISH_OB",

                    "high":
                        high,

                    "low":
                        low,

                    "index":
                        i,

                    "time":
                        current[3],

                })



        return {


            "bullish_order_blocks":

                bullish_blocks,


            "bearish_order_blocks":

                bearish_blocks,

        }
