
from typing import List, Dict


class RangeEngine:


    def accumulation(self, candles: List[Dict]) -> bool:

        if len(candles) < 20:
            return False

        try:

            ranges = [
                float(c["high"]) - float(c["low"])
                for c in candles[-20:]
            ]

            avg_range = sum(ranges) / len(ranges)

            return avg_range < (
                max(ranges) * 0.6
            )

        except Exception:
            return False



    def consolidation(self, candles: List[Dict]) -> bool:

        if len(candles) < 15:
            return False

        try:

            highs = [
                float(c["high"])
                for c in candles[-15:]
            ]

            lows = [
                float(c["low"])
                for c in candles[-15:]
            ]


            width = (
                max(highs)
                -
                min(lows)
            )

            price = float(
                candles[-1]["close"]
            )


            return (
                width / price
            ) < 0.03


        except Exception:

            return False




    def range_breakout(self, candles: List[Dict]) -> bool:

        if len(candles) < 20:
            return False


        try:

            highs=[
                float(c["high"])
                for c in candles[-20:-1]
            ]

            lows=[
                float(c["low"])
                for c in candles[-20:-1]
            ]


            last=float(
                candles[-1]["close"]
            )


            return (
                last > max(highs)
                or
                last < min(lows)
            )


        except Exception:

            return False





    def fake_breakout(self, candles: List[Dict]) -> bool:


        if len(candles)<20:
            return False


        try:

            highs=[
                float(c["high"])
                for c in candles[-20:-1]
            ]

            lows=[
                float(c["low"])
                for c in candles[-20:-1]
            ]


            last=candles[-1]


            high=float(last["high"])
            low=float(last["low"])
            close=float(last["close"])


            return (
                high > max(highs)
                and close < max(highs)
            ) or (
                low < min(lows)
                and close > min(lows)
            )


        except Exception:

            return False





    def return_to_range(self, candles: List[Dict]) -> bool:

        if len(candles)<10:
            return False


        try:

            highs=[
                float(c["high"])
                for c in candles[-10:]
            ]

            lows=[
                float(c["low"])
                for c in candles[-10:]
            ]

            current=float(
                candles[-1]["close"]
            )


            return (
                min(highs)
                <
                current
                <
                max(highs)
            )


        except Exception:

            return False




    def analyze(self, candles):

        reasons=[]

        score=0


        if self.accumulation(candles):

            score+=20
            reasons.append(
                "ACCUMULATION"
            )


        if self.consolidation(candles):

            score+=20
            reasons.append(
                "CONSOLIDATION"
            )


        if self.range_breakout(candles):

            score+=25
            reasons.append(
                "RANGE BREAKOUT"
            )


        if self.fake_breakout(candles):

            score+=20
            reasons.append(
                "FALSE RANGE BREAK"
            )


        if self.return_to_range(candles):

            score+=15
            reasons.append(
                "RETURN TO RANGE"
            )


        return {

            "score": min(score,100),

            "reasons": reasons

        }

