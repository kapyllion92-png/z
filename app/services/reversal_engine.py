
class ReversalEngine:


    def after_pump(self, candles):

        if len(candles) < 20:
            return False

        try:

            start = float(candles[-20]["close"])
            current = float(candles[-1]["close"])

            growth = (
                current - start
            ) / start


            return growth > 0.15


        except Exception:

            return False



    def after_dump(self, candles):

        if len(candles) < 20:
            return False

        try:

            start = float(candles[-20]["close"])
            current = float(candles[-1]["close"])

            drop = (
                start - current
            ) / start


            return drop > 0.15


        except Exception:

            return False



    def liquidity_reversal(self, candles):

        if len(candles) < 5:
            return False

        try:

            prev = candles[-2]
            last = candles[-1]


            return (

                (
                    float(last["low"])
                    <
                    float(prev["low"])
                    and
                    float(last["close"])
                    >
                    float(prev["low"])
                )

                or

                (
                    float(last["high"])
                    >
                    float(prev["high"])
                    and
                    float(last["close"])
                    <
                    float(prev["high"])
                )

            )


        except Exception:

            return False



    def level_reversal(self, candles):

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


            last = float(
                candles[-1]["close"]
            )


            resistance = max(highs)
            support = min(lows)


            return (
                abs(last-resistance)/resistance < 0.003
                or
                abs(last-support)/support < 0.003
            )


        except Exception:

            return False



    def v_reversal(self, candles):

        if len(candles) < 7:
            return False

        try:

            lows = [
                float(x["low"])
                for x in candles[-7:]
            ]


            middle = min(lows)


            return (
                float(candles[-1]["close"])
                >
                float(candles[-3]["close"])
                and
                float(candles[-3]["low"])
                ==
                middle
            )


        except Exception:

            return False



    def double_top(self, candles):

        if len(candles) < 10:
            return False

        try:

            highs = [
                float(x["high"])
                for x in candles[-10:]
            ]


            first = highs[:5]
            second = highs[5:]


            return (
                abs(
                    max(first)-max(second)
                )
                /
                max(first)
                <
                0.005
            )


        except Exception:

            return False



    def double_bottom(self, candles):

        if len(candles) < 10:
            return False

        try:

            lows = [
                float(x["low"])
                for x in candles[-10:]
            ]


            first = lows[:5]
            second = lows[5:]


            return (
                abs(
                    min(first)-min(second)
                )
                /
                min(first)
                <
                0.005
            )


        except Exception:

            return False



    def head_shoulders(self, candles):

        if len(candles) < 15:
            return False

        try:

            highs = [
                float(x["high"])
                for x in candles[-15:]
            ]


            left = max(highs[:5])
            head = max(highs[5:10])
            right = max(highs[10:])


            return (
                head > left
                and
                head > right
                and
                abs(left-right)/head < 0.03
            )


        except Exception:

            return False



    def analyze(self, candles):

        score = 0
        signals = []


        checks = {

            "AFTER PUMP":
                self.after_pump(candles),

            "AFTER DUMP":
                self.after_dump(candles),

            "LIQUIDITY REVERSAL":
                self.liquidity_reversal(candles),

            "LEVEL REVERSAL":
                self.level_reversal(candles),

            "V REVERSAL":
                self.v_reversal(candles),

            "DOUBLE TOP":
                self.double_top(candles),

            "DOUBLE BOTTOM":
                self.double_bottom(candles),

            "HEAD SHOULDERS":
                self.head_shoulders(candles)

        }


        for name, value in checks.items():

            if value:

                score += 15

                signals.append(name)


        return {

            "score":
                min(score,100),

            "signals":
                signals

        }

