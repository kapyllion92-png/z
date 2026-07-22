from typing import Dict, List


class LiquidityEngine:


    def analyze(self, candles: List[Dict]):

        result = {

            "liquidity_sweep": False,
            "stop_hunt": False,
            "equal_highs": False,
            "equal_lows": False,
            "liquidity_grab": False,
            "stop_run": False,
            "return_after_sweep": False,

            "direction": None,
            "score": 0,
            "reasons": []
        }


        if len(candles) < 10:
            return result


        highs = [
            float(c["high"])
            for c in candles
        ]

        lows = [
            float(c["low"])
            for c in candles
        ]


        closes = [
            float(c["close"])
            for c in candles
        ]


        last_high = highs[-1]
        last_low = lows[-1]
        last_close = closes[-1]


        prev_high = max(
            highs[-10:-1]
        )

        prev_low = min(
            lows[-10:-1]
        )


        # =========================
        # LIQUIDITY SWEEP
        # =========================

        if last_high > prev_high and last_close < prev_high:

            result["liquidity_sweep"] = True
            result["direction"] = "BEARISH"

            result["score"] += 20
            result["reasons"].append(
                "LIQUIDITY SWEEP HIGH"
            )


        if last_low < prev_low and last_close > prev_low:

            result["liquidity_sweep"] = True
            result["direction"] = "BULLISH"

            result["score"] += 20
            result["reasons"].append(
                "LIQUIDITY SWEEP LOW"
            )



        # =========================
        # STOP HUNT
        # =========================

        if last_high > prev_high:

            result["stop_hunt"] = True

            result["score"] += 10

            result["reasons"].append(
                "STOP HUNT"
            )


        if last_low < prev_low:

            result["stop_hunt"] = True

            result["score"] += 10

            result["reasons"].append(
                "STOP HUNT"
            )



        # =========================
        # EQUAL HIGHS
        # =========================

        recent_highs = highs[-5:]

        if max(recent_highs) - min(recent_highs) < (
            max(recent_highs) * 0.001
        ):

            result["equal_highs"] = True

            result["score"] += 10

            result["reasons"].append(
                "EQUAL HIGHS LIQUIDITY"
            )



        # =========================
        # EQUAL LOWS
        # =========================

        recent_lows = lows[-5:]

        if max(recent_lows) - min(recent_lows) < (
            max(recent_lows) * 0.001
        ):

            result["equal_lows"] = True

            result["score"] += 10

            result["reasons"].append(
                "EQUAL LOWS LIQUIDITY"
            )



        # =========================
        # LIQUIDITY GRAB
        # =========================

        if result["liquidity_sweep"]:

            result["liquidity_grab"] = True

            result["score"] += 10

            result["reasons"].append(
                "LIQUIDITY GRAB"
            )



        # =========================
        # STOP RUN
        # =========================

        if result["stop_hunt"] and result["liquidity_sweep"]:

            result["stop_run"] = True

            result["score"] += 10

            result["reasons"].append(
                "STOP RUN"
            )



        # =========================
        # RETURN AFTER SWEEP
        # =========================

        if result["liquidity_sweep"]:

            if (
                result["direction"] == "BULLISH"
                and last_close > prev_low
            ):

                result["return_after_sweep"] = True

                result["score"] += 10

                result["reasons"].append(
                    "RETURN AFTER LIQUIDITY SWEEP"
                )


            if (
                result["direction"] == "BEARISH"
                and last_close < prev_high
            ):

                result["return_after_sweep"] = True

                result["score"] += 10

                result["reasons"].append(
                    "RETURN AFTER LIQUIDITY SWEEP"
                )



        return result
