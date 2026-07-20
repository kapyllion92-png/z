from app.services.signal import Signal


class FakeBreakoutScanner:


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



        resistance = max(
            highs[-20:-1]
        )


        support = min(
            lows[-20:-1]
        )



        last_high = highs[-1]

        last_low = lows[-1]



        # Ложный пробой вверх


        if last_high > resistance and current < resistance:


            return Signal(

                symbol=symbol,

                direction="SHORT",

                strength=82,

                setup="FAKE BREAKOUT ВВЕРХ",

                reasons=[

                    "Пробит максимум",

                    "Цена вернулась под уровень",

                    "Возможная ловушка покупателей",

                    "Вероятный разворот вниз"

                ],

                entry=current,

                stop=last_high,

                target=support

            )



        # Ложный пробой вниз


        if last_low < support and current > support:


            return Signal(

                symbol=symbol,

                direction="LONG",

                strength=82,

                setup="FAKE BREAKOUT ВНИЗ",

                reasons=[

                    "Пробита поддержка",

                    "Цена вернулась выше уровня",

                    "Возможная ловушка продавцов",

                    "Вероятный разворот вверх"

                ],

                entry=current,

                stop=last_low,

                target=resistance

            )



        return None

