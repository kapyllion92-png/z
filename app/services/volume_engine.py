
from typing import List, Dict


class VolumeEngine:


    def volume_spike(self, candles: List[Dict]):

        if len(candles) < 20:
            return False

        try:

            volumes = [
                float(c["volume"])
                for c in candles[-20:-1]
            ]

            avg = sum(volumes) / len(volumes)

            last = float(
                candles[-1]["volume"]
            )

            return last > avg * 2


        except Exception:

            return False




    def abnormal_volume(self, candles: List[Dict]):

        if len(candles) < 30:
            return False

        try:

            volumes=[
                float(c["volume"])
                for c in candles[-30:-1]
            ]

            avg=sum(volumes)/len(volumes)

            last=float(
                candles[-1]["volume"]
            )


            return last > avg * 3


        except Exception:

            return False




    def buying_climax(self, candles: List[Dict]):

        if len(candles)<5:
            return False

        try:

            last=candles[-1]

            volume=float(
                last["volume"]
            )

            body=(
                float(last["close"])
                -
                float(last["open"])
            )


            return (
                body > 0
                and
                volume >
                float(candles[-2]["volume"]) * 2
            )


        except Exception:

            return False





    def selling_climax(self, candles: List[Dict]):

        if len(candles)<5:
            return False

        try:

            last=candles[-1]

            volume=float(
                last["volume"]
            )

            body=(
                float(last["open"])
                -
                float(last["close"])
            )


            return (
                body > 0
                and
                volume >
                float(candles[-2]["volume"]) * 2
            )


        except Exception:

            return False




    def absorption(self, candles: List[Dict]):

        if len(candles)<10:
            return False

        try:

            last=candles[-1]


            body=abs(
                float(last["close"])
                -
                float(last["open"])
            )


            volume=float(
                last["volume"]
            )


            return (
                volume > 0
                and
                body / volume < 0.001
            )


        except Exception:

            return False




    def accumulation(self, candles: List[Dict]):

        if len(candles)<20:
            return False

        try:

            prices=[
                float(c["close"])
                for c in candles[-20:]
            ]

            volumes=[
                float(c["volume"])
                for c in candles[-20:]
            ]


            price_change=(
                max(prices)-min(prices)
            )

            volume_growth=(
                volumes[-1]
                >
                sum(volumes[:-1])
                /
                len(volumes[:-1])
            )


            return (
                price_change < prices[-1]*0.03
                and
                volume_growth
            )


        except Exception:

            return False




    def distribution(self, candles: List[Dict]):

        if len(candles)<20:
            return False


        try:

            highs=[
                float(c["high"])
                for c in candles[-20:]
            ]

            volumes=[
                float(c["volume"])
                for c in candles[-20:]
            ]


            near_high = (
                float(candles[-1]["close"])
                >
                max(highs)*0.97
            )


            high_volume = (
                volumes[-1]
                >
                sum(volumes[:-1])
                /
                len(volumes[:-1])
            )


            return (
                near_high
                and
                high_volume
            )


        except Exception:

            return False




    def analyze(self, candles):

        score=0
        signals=[]


        checks={

            "VOLUME SPIKE":
                self.volume_spike(candles),

            "ABNORMAL VOLUME":
                self.abnormal_volume(candles),

            "BUYING CLIMAX":
                self.buying_climax(candles),

            "SELLING CLIMAX":
                self.selling_climax(candles),

            "ABSORPTION":
                self.absorption(candles),

            "ACCUMULATION":
                self.accumulation(candles),

            "DISTRIBUTION":
                self.distribution(candles)

        }


        for name,value in checks.items():

            if value:

                score += 15
                signals.append(name)


        return {

            "score":
                min(score,100),

            "signals":
                signals

        }

