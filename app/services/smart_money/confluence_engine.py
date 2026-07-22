from typing import Dict


class ConfluenceEngine:


    def analyze(self, modules: Dict) -> Dict:


        score = 0
        reasons = []
        confirmations = 0


        structure = modules.get("structure", {})
        liquidity = modules.get("liquidity", {})
        fvg = modules.get("fvg", {})
        order_block = modules.get("order_block", {})
        zone = modules.get("zone", {})
        breakout = modules.get("breakout", {})
        reversal = modules.get("reversal", {})
        volume = modules.get("volume", {})
        candle = modules.get("candle", {})
        volatility = modules.get("volatility", {})



        # ==========================
        # STRUCTURE
        # ==========================

        if structure.get("higher_high"):

            score += 10
            confirmations += 1

            reasons.append(
                "HIGHER HIGH"
            )


        if structure.get("higher_low"):

            score += 10
            confirmations += 1

            reasons.append(
                "HIGHER LOW"
            )


        if structure.get("bos"):

            score += 15
            confirmations += 1

            reasons.append(
                "BULLISH BOS"
            )


        if structure.get("choch"):

            score += 10
            confirmations += 1

            reasons.append(
                "CHoCH"
            )



        # ==========================
        # LIQUIDITY
        # ==========================

        if liquidity.get("liquidity_sweep"):

            score += 20
            confirmations += 1

            reasons.append(
                "LIQUIDITY SWEEP"
            )


        if liquidity.get("liquidity_grab"):

            score += 15
            confirmations += 1

            reasons.append(
                "LIQUIDITY GRAB"
            )


        if liquidity.get("stop_hunt"):

            score += 15
            confirmations += 1

            reasons.append(
                "STOP HUNT"
            )



        # ==========================
        # FVG
        # ==========================

        if fvg.get("imbalance"):

            score += 10

            reasons.append(
                "Imbalance"
            )


        if fvg.get("fair_value_gap"):

            score += 10

            reasons.append(
                "Fair Value Gap"
            )



        # ==========================
        # ORDER BLOCK
        # ==========================

        if order_block.get("bullish_ob"):

            score += 15

            reasons.append(
                "BULLISH ORDER BLOCK"
            )


        if order_block.get("bearish_ob"):

            score += 15

            reasons.append(
                "BEARISH ORDER BLOCK"
            )


        if order_block.get("mitigation"):

            score += 10

            reasons.append(
                "MITIGATION BLOCK"
            )


        if order_block.get("breaker_block"):

            score += 10

            reasons.append(
                "BREAKER BLOCK"
            )



        # ==========================
        # BREAKOUT
        # ==========================

        if breakout.get("true_breakout"):

            score += 20

            reasons.append(
                "TRUE BREAKOUT"
            )


        if breakout.get("false_breakout"):

            score += 10

            reasons.append(
                "FALSE BREAKOUT"
            )


        if breakout.get("retest"):

            score += 10

            reasons.append(
                "BREAKOUT RETEST"
            )



        # ==========================
        # REVERSAL
        # ==========================

        if reversal.get("confirmation"):

            score += 15

            reasons.append(
                "REVERSAL CONFIRMATION"
            )



        # ==========================
        # VOLUME
        # ==========================

        if volume.get("volume_spike"):

            score += 15

            reasons.append(
                "VOLUME SPIKE"
            )


        if volume.get("abnormal_volume"):

            score += 10

            reasons.append(
                "ABNORMAL VOLUME"
            )


        if volume.get("absorption"):

            score += 15

            reasons.append(
                "VOLUME ABSORPTION"
            )


        if volume.get("accumulation"):

            score += 10

            reasons.append(
                "ACCUMULATION"
            )


        if volume.get("distribution"):

            score += 10

            reasons.append(
                "DISTRIBUTION"
            )


        if volume.get("volume_confirmation"):

            score += 10

            reasons.append(
                "VOLUME CONFIRMATION"
            )



        # ==========================
        # VOLATILITY
        # ==========================

        if volatility.get("atr_expansion"):

            score += 10

            reasons.append(
                "ATR EXPANSION"
            )


        if volatility.get("atr_squeeze"):

            score += 5

            reasons.append(
                "ATR SQUEEZE"
            )


        if volatility.get("bollinger_squeeze"):

            score += 10

            reasons.append(
                "BOLLINGER SQUEEZE"
            )


        if volatility.get("squeeze_breakout"):

            score += 15

            reasons.append(
                "SQUEEZE BREAKOUT"
            )




        # ==========================
        # CANDLE PATTERNS
        # ==========================

        if candle.get("bullish_engulfing"):

            score += 15
            reasons.append(
                "BULLISH ENGULFING"
            )


        if candle.get("bearish_engulfing"):

            score += 15
            reasons.append(
                "BEARISH ENGULFING"
            )


        if candle.get("hammer"):

            score += 10
            reasons.append(
                "HAMMER"
            )


        if candle.get("shooting_star"):

            score += 10
            reasons.append(
                "SHOOTING STAR"
            )


        if candle.get("bullish_pin_bar"):

            score += 10
            reasons.append(
                "BULLISH PIN BAR"
            )


        if candle.get("bearish_pin_bar"):

            score += 10
            reasons.append(
                "BEARISH PIN BAR"
            )


        if candle.get("morning_star"):

            score += 15
            reasons.append(
                "MORNING STAR"
            )


        if candle.get("evening_star"):

            score += 15
            reasons.append(
                "EVENING STAR"
            )


        if candle.get("three_white_soldiers"):

            score += 20
            reasons.append(
                "THREE WHITE SOLDIERS"
            )


        if candle.get("three_black_crows"):

            score += 20
            reasons.append(
                "THREE BLACK CROWS"
            )


        if candle.get("inside_bar"):

            score += 5
            reasons.append(
                "INSIDE BAR"
            )


        if candle.get("outside_bar"):

            score += 10
            reasons.append(
                "OUTSIDE BAR"
            )


        if candle.get("body_strength") == "STRONG":

            score += 5
            reasons.append(
                "STRONG BODY"
            )



        # ==========================
        # DIRECTION
        # ==========================

        direction = None


        if (
            structure.get("higher_high")
            and
            structure.get("higher_low")
            and
            structure.get("bos")
        ):

            direction = "LONG"


        if (
            structure.get("lower_low")
            and
            structure.get("lower_high")
            and
            structure.get("bearish_bos")
        ):

            direction = "SHORT"



        if score >= 70:

            grade = "A SETUP"

        elif score >= 55:

            grade = "B SETUP"

        elif score >= 40:

            grade = "C SETUP"

        else:

            grade = "NO SETUP"



        return {

            "direction": direction,

            "score": score,

            "grade": grade,

            "reasons": reasons,

            "confirmations": confirmations

        }
