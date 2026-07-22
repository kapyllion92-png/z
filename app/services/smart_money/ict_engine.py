from typing import List, Dict


class ICTEngine:

    def __init__(self):
        pass


    def _highs(self, candles):
        return [float(c["high"]) for c in candles]


    def _lows(self, candles):
        return [float(c["low"]) for c in candles]


    def _closes(self, candles):
        return [float(c["close"]) for c in candles]


    # ==========================
    # BOS
    # ==========================

    def bos(self, candles):

        if len(candles) < 10:
            return False

        highs = self._highs(candles[-10:])
        lows = self._lows(candles[-10:])
        close = float(candles[-1]["close"])

        return (
            close > max(highs[:-1])
            or
            close < min(lows[:-1])
        )


    # ==========================
    # CHoCH
    # ==========================

    def choch(self, candles):

        if len(candles) < 20:
            return False

        last = float(candles[-1]["close"])
        previous = float(candles[-10]["close"])

        return abs(last - previous) > 0


    # ==========================
    # Equal Highs / Equal Lows
    # ==========================

    def equal_highs(self, candles):

        highs = self._highs(candles[-20:])

        if len(highs) < 5:
            return False

        return abs(
            max(highs[-5:])
            -
            sorted(highs[-5:])[-2]
        ) < max(highs) * 0.001


    def equal_lows(self, candles):

        lows = self._lows(candles[-20:])

        if len(lows) < 5:
            return False

        return abs(
            min(lows[-5:])
            -
            sorted(lows[-5:])[1]
        ) < max(lows) * 0.001


    # ==========================
    # Liquidity Sweep
    # ==========================

    def liquidity_sweep(self, candles):

        if len(candles) < 5:
            return False

        previous = candles[-2]
        current = candles[-1]

        return (
            float(current["high"]) > float(previous["high"])
            and
            float(current["close"]) < float(previous["high"])
        ) or (
            float(current["low"]) < float(previous["low"])
            and
            float(current["close"]) > float(previous["low"])
        )


    # ==========================
    # Stop Hunt
    # ==========================

    def stop_hunt(self, candles):

        return (
            self.liquidity_sweep(candles)
            and
            (self.equal_highs(candles) or self.equal_lows(candles))
        )


    # ==========================
    # Order Block
    # ==========================

    def order_block(self, candles):

        if len(candles) < 5:
            return {
                "found": False
            }

        last = candles[-1]
        prev = candles[-2]

        bullish = (
            float(last["close"])
            >
            float(prev["high"])
        )

        bearish = (
            float(last["close"])
            <
            float(prev["low"])
        )


        if bullish:

            return {
                "found": True,
                "type": "BULLISH OB",
                "score": 15
            }


        if bearish:

            return {
                "found": True,
                "type": "BEARISH OB",
                "score": 15
            }


        return {
            "found": False
        }


    # ==========================
    # Fair Value Gap
    # ==========================

    def fair_value_gap(self, candles):

        if len(candles) < 3:
            return False


        c1 = candles[-3]
        c3 = candles[-1]


        return (
            float(c1["high"])
            <
            float(c3["low"])
        ) or (
            float(c1["low"])
            >
            float(c3["high"])
        )


    # ==========================
    # Imbalance
    # ==========================

    def imbalance(self, candles):

        return self.fair_value_gap(candles)


    # ==========================
    # Breaker Block
    # ==========================

    def breaker_block(self, candles):

        return (
            self.bos(candles)
            and
            self.order_block(candles).get("found")
        )


    # ==========================
    # Mitigation Block
    # ==========================

    def mitigation_block(self, candles):

        return (
            self.order_block(candles).get("found")
            and
            self.liquidity_sweep(candles)
        )


    # ==========================
    # Premium / Discount
    # ==========================

    def premium_discount(self, candles):

        highs = self._highs(candles[-20:])
        lows = self._lows(candles[-20:])

        high = max(highs)
        low = min(lows)

        mid = (high + low) / 2

        price = float(candles[-1]["close"])


        if price < mid:
            return "DISCOUNT"

        return "PREMIUM"


    # ==========================
    # OTE Zone
    # ==========================

    def ote_zone(self, candles):

        highs = self._highs(candles[-20:])
        lows = self._lows(candles[-20:])


        high = max(highs)
        low = min(lows)

        fib62 = high - (high-low)*0.62
        fib79 = high - (high-low)*0.79

        price = float(candles[-1]["close"])


        return fib79 <= price <= fib62


    # ==========================
    # FINAL CONFLUENCE
    # ==========================

    def analyze(self, candles):

        score = 0
        reasons = []


        checks = [

            (self.bos(candles),10,"BOS"),
            (self.choch(candles),10,"CHoCH"),
            (self.liquidity_sweep(candles),15,"Liquidity Sweep"),
            (self.stop_hunt(candles),15,"Stop Hunt"),
            (self.equal_highs(candles),5,"Equal Highs"),
            (self.equal_lows(candles),5,"Equal Lows"),
            (self.fair_value_gap(candles),10,"Fair Value Gap"),
            (self.imbalance(candles),10,"Imbalance"),
            (self.breaker_block(candles),10,"Breaker Block"),
            (self.mitigation_block(candles),10,"Mitigation Block"),
            (self.ote_zone(candles),10,"OTE Zone")

        ]


        for active, points, name in checks:

            if active:
                score += points
                reasons.append(name)


        ob = self.order_block(candles)


        if ob.get("found"):

            score += ob.get("score",0)
            reasons.append(ob["type"])


        zone = self.premium_discount(candles)

        reasons.append(zone + " Zone")


        if score > 100:
            score = 100


        return {

            "score": score,

            "reasons": reasons,

            "order_block": ob,

            "zone": zone

        }
