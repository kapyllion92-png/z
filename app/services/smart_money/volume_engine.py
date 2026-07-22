from typing import Dict, List


class VolumeEngine:


    def analyze(self, candles: List[Dict]) -> Dict:

        result = {
            "volume_spike": False,
            "abnormal_volume": False,
            "buying_climax": False,
            "selling_climax": False,
            "absorption": False,
            "accumulation": False,
            "distribution": False,
            "volume_confirmation": False,
            "score": 0,
            "reasons": []
        }


        if len(candles) < 30:
            return result


        closes = [
            float(c["close"])
            for c in candles
        ]

        opens = [
            float(c["open"])
            for c in candles
        ]

        highs = [
            float(c["high"])
            for c in candles
        ]

        lows = [
            float(c["low"])
            for c in candles
        ]

        volumes = [
            float(c.get("volume", 0))
            for c in candles
        ]


        last_close = closes[-1]
        last_open = opens[-1]

        last_high = highs[-1]
        last_low = lows[-1]

        last_volume = volumes[-1]


        avg_volume = (
            sum(volumes[-20:-1]) / 19
            if sum(volumes[-20:-1]) > 0
            else 0
        )


        candle_size = last_high - last_low


        avg_range = (
            sum(
                highs[i] - lows[i]
                for i in range(-20, -1)
            ) / 19
        )



        # ==========================
        # VOLUME SPIKE
        # ==========================

        if (
            avg_volume > 0
            and
            last_volume > avg_volume * 1.8
        ):

            result["volume_spike"] = True
            result["score"] += 15

            result["reasons"].append(
                "VOLUME SPIKE"
            )



        # ==========================
        # ABNORMAL VOLUME
        # ==========================

        if (
            avg_volume > 0
            and
            last_volume > avg_volume * 2.5
        ):

            result["abnormal_volume"] = True
            result["score"] += 10

            result["reasons"].append(
                "ABNORMAL VOLUME"
            )



        # ==========================
        # BUYING CLIMAX
        # ==========================

        if (
            last_close > last_open
            and
            last_volume > avg_volume * 2
            and
            candle_size > avg_range * 1.5
        ):

            result["buying_climax"] = True
            result["score"] += 10

            result["reasons"].append(
                "BUYING CLIMAX"
            )



        # ==========================
        # SELLING CLIMAX
        # ==========================

        if (
            last_close < last_open
            and
            last_volume > avg_volume * 2
            and
            candle_size > avg_range * 1.5
        ):

            result["selling_climax"] = True
            result["score"] += 10

            result["reasons"].append(
                "SELLING CLIMAX"
            )



        # ==========================
        # ABSORPTION
        # ==========================

        if (
            last_volume > avg_volume * 1.5
            and
            candle_size < avg_range * 0.7
        ):

            result["absorption"] = True
            result["score"] += 15

            result["reasons"].append(
                "VOLUME ABSORPTION"
            )



        # ==========================
        # ACCUMULATION
        # ==========================

        small_volume = 0


        for i in range(-15, -5):

            if (
                volumes[i] < avg_volume
                and
                (highs[i] - lows[i]) < avg_range
            ):
                small_volume += 1


        if small_volume >= 5:

            result["accumulation"] = True
            result["score"] += 10

            result["reasons"].append(
                "ACCUMULATION"
            )



        # ==========================
        # DISTRIBUTION
        # ==========================

        red_candles = 0


        for i in range(-10, -1):

            if closes[i] < opens[i]:
                red_candles += 1


        if (
            red_candles >= 6
            and
            last_volume > avg_volume
        ):

            result["distribution"] = True
            result["score"] += 10

            result["reasons"].append(
                "DISTRIBUTION"
            )



        # ==========================
        # VOLUME CONFIRMATION
        # ==========================

        if (
            result["volume_spike"]
            or
            result["abnormal_volume"]
        ):

            result["volume_confirmation"] = True

            result["score"] += 10

            result["reasons"].append(
                "VOLUME CONFIRMATION"
            )



        return result
