from typing import Dict


class SignalIntelligence:


    def analyze(self, modules: Dict, score: int):

        confidence = 0
        reasons = []
        warnings = []


        structure = modules.get("structure", {})
        candle = modules.get("candle", {})
        volume = modules.get("volume", {})
        volatility = modules.get("volatility", {})
        liquidity = modules.get("liquidity", {})



        # ======================
        # STRUCTURE CONFIRMATION
        # ======================

        if structure.get("higher_high"):

            confidence += 10
            reasons.append(
                "BULLISH STRUCTURE"
            )


        if structure.get("higher_low"):

            confidence += 10
            reasons.append(
                "HIGHER LOW SUPPORT"
            )


        if structure.get("bos"):

            confidence += 15
            reasons.append(
                "BOS CONFIRMATION"
            )


        if structure.get("bearish_bos"):

            confidence -= 15
            warnings.append(
                "BEARISH BOS"
            )



        # ======================
        # CANDLE AGREEMENT
        # ======================

        if candle.get("direction") == "BULLISH":

            confidence += 10
            reasons.append(
                "BULLISH CANDLE"
            )


        if candle.get("direction") == "BEARISH":

            confidence -= 10
            warnings.append(
                "BEARISH CANDLE"
            )


        if candle.get("bullish_engulfing"):

            confidence += 15
            reasons.append(
                "BULLISH ENGULFING"
            )


        if candle.get("bearish_engulfing"):

            confidence -= 15
            warnings.append(
                "BEARISH ENGULFING"
            )



        # ======================
        # VOLUME
        # ======================

        if volume.get("accumulation"):

            confidence += 10
            reasons.append(
                "ACCUMULATION"
            )


        if volume.get("distribution"):

            confidence -= 10
            warnings.append(
                "DISTRIBUTION"
            )



        # ======================
        # VOLATILITY
        # ======================

        if volatility.get("atr_expansion"):

            confidence += 10
            reasons.append(
                "ATR EXPANSION"
            )


        if volatility.get("squeeze_breakout"):

            confidence += 15
            reasons.append(
                "SQUEEZE BREAKOUT"
            )



        # ======================
        # LIQUIDITY
        # ======================

        if liquidity.get("liquidity_sweep"):

            confidence += 15
            reasons.append(
                "LIQUIDITY SWEEP"
            )



        confidence += min(score // 5, 30)


        if confidence > 100:
            confidence = 100


        if confidence >= 85:

            quality = "A+ SETUP"

        elif confidence >= 70:

            quality = "A SETUP"

        elif confidence >= 55:

            quality = "B SETUP"

        else:

            quality = "LOW QUALITY"



        return {

            "confidence": confidence,

            "quality": quality,

            "reasons": reasons,

            "warnings": warnings

        }
