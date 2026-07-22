from app.services.signal import Signal


class PumpScanner:


    def scan(self, symbol, candles):

        try:

            if len(candles) < 30:
                return None


            closes = [
                float(c[4])
                for c in candles
            ]


            volumes = [
                float(c[5])
                for c in candles
            ]


            price = closes[-1]

            old_price = closes[-25]


            change = (
                (price - old_price)
                /
                old_price
                *
                100
            )


            avg_volume = (
                sum(volumes[-25:])
                /
                25
            )


            volume_power = (
                volumes[-1]
                /
                avg_volume
                if avg_volume > 0
                else 0
            )


            strength = 0

            reasons = []


            if change >= 3:

                strength += 30

                reasons.append(
                    "Рост более 3%"
                )


            if volume_power >= 1.5:

                strength += 25

                reasons.append(
                    "Повышенный объём"
                )


            if closes[-1] < closes[-2]:

                strength += 20

                reasons.append(
                    "Появился продавец после пампа"
                )


            if strength < 60:

                return None



            entry = price

            stop = price * 1.015

            target = price * 0.97



            return Signal(

                symbol=symbol,

                direction="SHORT",

                strength=min(
                    strength,
                    100
                ),

                setup=
                "Снайпер: отскок после пампа",

                reasons=reasons,

                entry=round(
                    entry,
                    8
                ),

                stop=round(
                    stop,
                    8
                ),

                target=round(
                    target,
                    8
                ),

                profit="3%",

                decision=
                "МОЖНО ГОТОВИТЬ ВХОД"
                if strength >= 75
                else
                "НАБЛЮДАТЬ",

                waiting=
                "15-25 минут"

            )


        except Exception:

            return None
