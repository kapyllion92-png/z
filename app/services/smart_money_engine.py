from typing import Dict, List

from app.services.smart_money.confluence_engine import ConfluenceEngine
from app.services.smart_money.direction_engine import DirectionEngine
from app.services.smart_money.reversal_engine import ReversalEngine
from app.services.smart_money.volume_engine import VolumeEngine
from app.services.smart_money.range_engine import RangeEngine
from app.services.smart_money.volatility_engine import VolatilityEngine
from app.services.smart_money.candle_engine import CandleEngine

try:
    from app.services.smart_money.structure_engine import StructureEngine
except:
    StructureEngine = None

try:
    from app.services.smart_money.liquidity_engine import LiquidityEngine
except:
    LiquidityEngine = None

try:
    from app.services.smart_money.fvg_engine import FVGEngine
except:
    FVGEngine = None

try:
    from app.services.smart_money.order_block_engine import OrderBlockEngine
except:
    OrderBlockEngine = None

try:
    from app.services.smart_money.zone_engine import ZoneEngine
except:
    ZoneEngine = None

try:
    from app.services.smart_money.breakout_engine import BreakoutEngine
except:
    BreakoutEngine = None

try:
    from app.services.smart_money.premium_discount_engine import PremiumDiscountEngine
except:
    PremiumDiscountEngine = None


class SmartMoneyEngine:

    def __init__(self):

        self.confluence = ConfluenceEngine()
        self.direction = DirectionEngine()

        self.reversal = ReversalEngine()
        self.volume = VolumeEngine()
        self.candle = CandleEngine()
        self.range = RangeEngine()
        self.volatility = VolatilityEngine()

        self.structure = StructureEngine() if StructureEngine else None
        self.liquidity = LiquidityEngine() if LiquidityEngine else None
        self.fvg = FVGEngine() if FVGEngine else None
        self.order_block = OrderBlockEngine() if OrderBlockEngine else None
        self.zone = ZoneEngine() if ZoneEngine else None
        self.breakout = BreakoutEngine() if BreakoutEngine else None
        self.premium_discount = PremiumDiscountEngine() if PremiumDiscountEngine else None


    def safe_analyze(self, engine, candles):

        if engine is None:
            return {}

        try:
            return engine.analyze(candles)

        except Exception as e:
            return {
                "error": str(e)
            }


    def modular_analysis(self, candles: List[Dict]) -> Dict:

        modules = {}

        modules["structure"] = self.safe_analyze(
            self.structure,
            candles
        )

        modules["liquidity"] = self.safe_analyze(
            self.liquidity,
            candles
        )

        modules["fvg"] = self.safe_analyze(
            self.fvg,
            candles
        )

        modules["order_block"] = self.safe_analyze(
            self.order_block,
            candles
        )

        modules["zone"] = self.safe_analyze(
            self.zone,
            candles
        )

        modules["breakout"] = self.safe_analyze(
            self.breakout,
            candles
        )

        modules["premium_discount"] = self.safe_analyze(
            self.premium_discount,
            candles
        )


        modules["reversal"] = self.safe_analyze(
            self.reversal,
            candles
        )

        modules["volume"] = self.safe_analyze(
            self.volume,
            candles
        )

        modules["volatility"] = self.safe_analyze(
            self.volatility,
            candles
        )

        modules["candle"] = self.safe_analyze(
            self.candle,
            candles
        )

        modules["range"] = self.safe_analyze(
            self.range,
            candles
        )


        confluence = self.confluence.analyze(
            modules
        )


        direction = self.direction.analyze(
            modules,
            confluence.get("score",0)
        )


        confluence["direction"] = direction.get(
            "direction"
        )

        confluence["confidence"] = direction.get(
            "confidence",
            0
        )

        confidence = direction.get(
            "confidence",
            0
        )

        try:
            confidence = int(confidence)
        except:
            confidence = 0

        try:
            confidence = int(confidence)
        except:
            confidence = 0

        if confidence >= 85:
            grade = "A+ SETUP"
        elif confidence >= 70:
            grade = "A SETUP"
        elif confidence >= 55:
            grade = "B SETUP"
        else:
            grade = "LOW QUALITY"

        confluence["grade"] = grade


        if direction.get("reasons"):

            confluence.setdefault(
                "reasons",
                []
            )

            confluence["reasons"].extend(
                direction["reasons"]
            )



        confluence["confidence"] = int(
            confluence.get("score", 0)
        )

        if confluence["confidence"] >= 85:
            confluence["grade"] = "A+ SETUP"
        elif confluence["confidence"] >= 70:
            confluence["grade"] = "A SETUP"
        elif confluence["confidence"] >= 55:
            confluence["grade"] = "B SETUP"
        else:
            confluence["grade"] = "LOW QUALITY"


        # ===============================
        # FINAL SIGNAL VALIDATOR
        # ===============================

        pd = modules.get("premium_discount", {})

        if confluence.get("direction") == "LONG":

            if pd.get("long_valid") is False:
                confluence["grade"] = "FILTERED"
                confluence["reasons"].append(
                    "LONG BLOCKED: PREMIUM ZONE"
                )
                confluence["trade_allowed"] = False
                confluence["grade"] = "FILTERED"

        elif confluence.get("direction") == "SHORT":

            if pd.get("short_valid") is False:
                confluence["grade"] = "FILTERED"
                confluence["reasons"].append(
                    "SHORT BLOCKED: DISCOUNT ZONE"
                )
                confluence["trade_allowed"] = False
                confluence["grade"] = "FILTERED"


        # ===============================
        # SIGNAL QUALITY ENGINE
        # ===============================

        raw_score = int(
            confluence.get("score", 0)
        )

        quality = min(
            100,
            max(
                0,
                raw_score
            )
        )

        confluence["quality"] = quality

        if quality >= 90:
            confluence["grade"] = "A+"
        elif quality >= 75:
            confluence["grade"] = "A"
        elif quality >= 60:
            confluence["grade"] = "B"
        elif quality >= 40:
            confluence["grade"] = "WEAK"
        else:
            confluence["grade"] = "BAD"

        # FINAL TRADE PERMISSION

        if confluence["grade"] == "FILTERED":
            confluence["trade_allowed"] = False
        else:
            confluence["trade_allowed"] = True

        confluence["modules"] = modules



        # ===============================
        # FINAL OVERRIDE CHECK
        # ===============================

        if any(
            "BLOCKED" in reason
            for reason in confluence.get("reasons", [])
        ):
            confluence["trade_allowed"] = False
            confluence["grade"] = "FILTERED"

        return confluence
