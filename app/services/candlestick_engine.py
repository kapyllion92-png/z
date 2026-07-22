
from typing import List, Dict


class CandlestickEngine:


    def body(self, candle):

        return abs(
            float(candle["close"])
            -
            float(candle["open"])
        )



    def upper_wick(self, candle):

        return (
            float(candle["high"])
            -
            max(
                float(candle["open"]),
                float(candle["close"])
            )
        )



    def lower_wick(self, candle):

        return (
            min(
                float(candle["open"]),
                float(candle["close"])
            )
            -
            float(candle["low"])
        )



    def doji(self, candle):

        try:

            body=self.body(candle)

            rng=(
                float(candle["high"])
                -
                float(candle["low"])
            )

            return (
                rng > 0
                and
                body/rng < 0.1
            )

        except Exception:

            return False



    def hammer(self, candle):

        try:

            body=self.body(candle)

            lower=self.lower_wick(candle)

            upper=self.upper_wick(candle)


            return (
                lower > body*2
                and
                upper < body
            )

        except Exception:

            return False




    def shooting_star(self, candle):

        try:

            body=self.body(candle)

            lower=self.lower_wick(candle)

            upper=self.upper_wick(candle)


            return (
                upper > body*2
                and
                lower < body
            )

        except Exception:

            return False





    def bullish_engulfing(self, candles):

        if len(candles)<2:
            return False


        try:

            prev=candles[-2]
            last=candles[-1]


            return (

                float(prev["close"])
                <
                float(prev["open"])

                and

                float(last["close"])
                >
                float(last["open"])

                and

                float(last["close"])
                >
                float(prev["open"])

                and

                float(last["open"])
                <
                float(prev["close"])

            )

        except Exception:

            return False





    def bearish_engulfing(self, candles):

        if len(candles)<2:
            return False


        try:

            prev=candles[-2]
            last=candles[-1]


            return (

                float(prev["close"])
                >
                float(prev["open"])

                and

                float(last["close"])
                <
                float(last["open"])

                and

                float(last["close"])
                <
                float(prev["open"])

                and

                float(last["open"])
                >
                float(prev["close"])

            )

        except Exception:

            return False





    def strong_candle(self, candle):

        try:

            body=self.body(candle)

            rng=(
                float(candle["high"])
                -
                float(candle["low"])
            )


            return (
                rng > 0
                and
                body/rng > 0.7
            )

        except Exception:

            return False





    def analyze(self, candles: List[Dict]):

        if len(candles)<2:

            return {
                "score":0,
                "signals":[]
            }


        score=0
        signals=[]


        last=candles[-1]


        checks={

            "DOJI":
                self.doji(last),

            "HAMMER":
                self.hammer(last),

            "SHOOTING_STAR":
                self.shooting_star(last),

            "BULLISH_ENGULFING":
                self.bullish_engulfing(candles),

            "BEARISH_ENGULFING":
                self.bearish_engulfing(candles),

            "STRONG_CANDLE":
                self.strong_candle(last)

        }


        for name,value in checks.items():

            if value:

                score+=20
                signals.append(name)



        return {

            "score":
                min(score,100),

            "signals":
                signals

        }

