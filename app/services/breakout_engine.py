
class BreakoutEngine:


    def true_breakout(self, candles):

        if len(candles) < 20:
            return False

        try:

            highs = [
                float(c["high"])
                for c in candles[-20:-1]
            ]

            last = candles[-1]

            return (
                float(last["close"]) > max(highs)
            )

        except Exception:

            return False



    def fake_breakout(self, candles):

        if len(candles) < 5:
            return False

        try:

            prev = candles[-2]
            last = candles[-1]


            return (
                float(last["high"]) > float(prev["high"])
                and
                float(last["close"]) < float(prev["high"])
            ) or (
                float(last["low"]) < float(prev["low"])
                and
                float(last["close"]) > float(prev["low"])
            )

        except Exception:

            return False



    def breakout_retest(self, candles):

        if len(candles) < 10:
            return False

        try:

            level = max(
                float(c["high"])
                for c in candles[-10:-3]
            )

            last = candles[-1]


            return (
                float(last["low"]) <= level
                and
                float(last["close"]) > level
            )

        except Exception:

            return False



    def accumulation_breakout(self, candles):

        if len(candles) < 20:
            return False

        try:

            ranges = []

            for c in candles[-20:-5]:

                ranges.append(
                    float(c["high"])
                    -
                    float(c["low"])
                )


            avg_range = sum(ranges) / len(ranges)


            last = candles[-1]

            return (
                (
                    float(last["high"])
                    -
                    float(last["low"])
                )
                >
                avg_range * 1.8
            )

        except Exception:

            return False



    def volume_breakout(self, candles):

        if len(candles) < 20:
            return False

        try:

            volumes = [
                float(c["volume"])
                for c in candles[-20:-1]
            ]

            avg_volume = sum(volumes) / len(volumes)


            last_volume = float(
                candles[-1]["volume"]
            )


            return last_volume > avg_volume * 2


        except Exception:

            return False



    def weak_breakout(self, candles):

        if len(candles) < 10:
            return False

        try:

            last = candles[-1]

            body = abs(
                float(last["close"])
                -
                float(last["open"])
            )

            candle_range = (
                float(last["high"])
                -
                float(last["low"])
            )


            if candle_range == 0:
                return False


            return (
                body / candle_range
            ) < 0.35


        except Exception:

            return False



    def analyze(self, candles):

        score = 0
        signals = []


        if self.true_breakout(candles):
            score += 25
            signals.append(
                "TRUE BREAKOUT"
            )


        if self.fake_breakout(candles):
            score += 20
            signals.append(
                "FAKE BREAKOUT"
            )


        if self.breakout_retest(candles):
            score += 15
            signals.append(
                "RETEST"
            )


        if self.accumulation_breakout(candles):
            score += 15
            signals.append(
                "ACCUMULATION BREAKOUT"
            )


        if self.volume_breakout(candles):
            score += 20
            signals.append(
                "HIGH VOLUME BREAKOUT"
            )


        if self.weak_breakout(candles):
            score -= 10
            signals.append(
                "WEAK BREAKOUT"
            )


        return {

            "score": max(
                min(score,100),
                0
            ),

            "signals": signals

        }

