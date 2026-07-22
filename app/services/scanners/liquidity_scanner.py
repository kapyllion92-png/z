from app.services.signal import Signal


class LiquidityScanner:


    def scan(self, symbol, candles):


        if len(candles) < 30:

            return None



        highs = [
            float(c[2])
            for c in candles
        ]


        lows = [
            float(c[3])
            for c in candles
        ]


        closes = [
            float(c[4])
            for c in candles
        ]



        current = closes[-1]



        previous_high = max(
            highs[-20:-1]
        )


        previous_low = min(
            lows[-20:-1]
        )



        last_high = highs[-1]

        last_low = lows[-1]



        # снятие ликвидности сверху

        if last_high > previous_high and current < previous_high:


            return Signal(

                symbol=symbol,

                direction="SHORT",

                strength=85,

                setup="LIQUIDITY SWEEP ВВЕРХ",

                reasons=[

                    "Снят верхний пул ликвидности",

                    "Стопы покупателей собраны",

                    "Цена вернулась под уровень",

                    "Вероятный разворот вниз"

                ],

                entry=current,

                stop=last_high,

                target=previous_low

            )




        # снятие ликвидности снизу


        if last_low < previous_low and current > previous_low:


            return Signal(

                symbol=symbol,

                direction="LONG",

                strength=85,

                setup="LIQUIDITY SWEEP ВНИЗ",

                reasons=[

                    "Снят нижний пул ликвидности",

                    "Стопы продавцов собраны",

                    "Цена вернулась выше уровня",

                    "Вероятный разворот вверх"

                ],

                entry=current,

                stop=last_low,

                target=previous_high

            )


        return None

