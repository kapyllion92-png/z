class SmartMoneyEngine:


    def liquidity_sweep(self, candles):

        if len(candles) < 20:
            return False


        highs = [
            float(c["high"])
            for c in candles
            if "high" in c
        ]

        lows = [
            float(c["low"])
            for c in candles
            if "low" in c
        ]


        if not highs or not lows:
            return False


        last_high = highs[-1]
        previous_high = max(highs[-10:-1])


        last_low = lows[-1]
        previous_low = min(lows[-10:-1])


        if last_high > previous_high:
            return True


        if last_low < previous_low:
            return True


        return False



    def equal_highs(self, candles):

        if len(candles) < 10:
            return False


        highs = [
            float(c["high"])
            for c in candles[-10:]
            if "high" in c
        ]


        if len(highs) < 5:
            return False


        return (
            max(highs) - min(highs)
        ) / max(highs) < 0.003



    def equal_lows(self, candles):

        if len(candles) < 10:
            return False


        lows = [
            float(c["low"])
            for c in candles[-10:]
            if "low" in c
        ]


        if len(lows) < 5:
            return False


        return (
            max(lows) - min(lows)
        ) / min(lows) < 0.003



    def fair_value_gap(self, candles):

        if len(candles) < 3:
            return False


        c1 = candles[-3]
        c3 = candles[-1]


        if "high" not in c1:
            return False


        if "low" not in c3:
            return False


        return (
            float(c3["low"])
            >
            float(c1["high"])
        )



    def analyze(self, candles):


        score = 0
        reasons = []


        if self.liquidity_sweep(candles):

            score += 25

            reasons.append(
                "Liquidity Sweep"
            )



        if self.equal_highs(candles):

            score += 10

            reasons.append(
                "Equal Highs"
            )



        if self.equal_lows(candles):

            score += 10

            reasons.append(
                "Equal Lows"
            )



        if self.fair_value_gap(candles):

            score += 20

            reasons.append(
                "Fair Value Gap"
            )



        return {

            "score": score,

            "reasons": reasons

        }
