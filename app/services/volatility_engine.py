
from typing import List, Dict


class VolatilityEngine:


    def atr_values(self, candles: List[Dict]):

        try:

            values=[]

            for c in candles[-20:]:

                high=float(c["high"])
                low=float(c["low"])

                values.append(
                    high-low
                )

            return values


        except Exception:

            return []




    def atr_squeeze(self, candles: List[Dict]):

        if len(candles)<20:
            return False


        try:

            atr=self.atr_values(candles)

            current=atr[-1]

            average=sum(atr)/len(atr)


            return current < average*0.6


        except Exception:

            return False





    def atr_expansion(self, candles: List[Dict]):

        if len(candles)<20:
            return False


        try:

            atr=self.atr_values(candles)

            current=atr[-1]

            average=sum(atr)/len(atr)


            return current > average*1.5


        except Exception:

            return False





    def bollinger_squeeze(self, candles: List[Dict]):

        if len(candles)<20:
            return False


        try:

            prices=[
                float(c["close"])
                for c in candles[-20:]
            ]


            mean=sum(prices)/len(prices)


            variance=sum(
                (x-mean)**2
                for x in prices
            )/len(prices)


            deviation=variance**0.5


            bandwidth=(
                deviation*2
            )/mean


            return bandwidth < 0.02


        except Exception:

            return False





    def breakout_from_squeeze(self, candles: List[Dict]):

        if len(candles)<25:
            return False


        try:

            squeeze=self.bollinger_squeeze(
                candles[:-1]
            )


            last=candles[-1]

            body=abs(
                float(last["close"])
                -
                float(last["open"])
            )


            candle_range=(
                float(last["high"])
                -
                float(last["low"])
            )


            if candle_range==0:
                return False


            strong_move = (
                body/candle_range
            ) > 0.7


            return (
                squeeze
                and
                strong_move
            )


        except Exception:

            return False





    def analyze(self, candles):

        score=0
        signals=[]


        checks={

            "ATR SQUEEZE":
                self.atr_squeeze(candles),

            "ATR EXPANSION":
                self.atr_expansion(candles),

            "BOLLINGER SQUEEZE":
                self.bollinger_squeeze(candles),

            "BREAKOUT FROM SQUEEZE":
                self.breakout_from_squeeze(candles)

        }


        for name,value in checks.items():

            if value:

                score+=25
                signals.append(name)


        return {

            "score":
                min(score,100),

            "signals":
                signals

        }

