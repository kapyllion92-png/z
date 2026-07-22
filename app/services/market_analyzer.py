from typing import Dict


class MarketAnalyzer:

    def __init__(self):
        pass


    def analyze(self, candles):

        result = {}

        market = {}

        final_smc = {
            "engine": "SMART MONEY DEFAULT",
            "error": "NOT INITIALIZED",
            "best_setup": {},
            "setups": []
        }


        try:
            from app.services.market_analyzer import MarketAnalyzer

        except:
            pass


        try:
            from app.services.smart_money.smart_money_fusion_engine import SmartMoneyFusionEngine

            smc = SmartMoneyFusionEngine()
            final_smc = smc.analyze(candles)

        except Exception as e:

            final_smc = {
                "engine": "SMART MONEY ERROR",
                "error": str(e),
                "best_setup": {},
                "setups": []
            }


        try:
            from app.services.indicator_engine import IndicatorEngine

            market = IndicatorEngine().analyze(candles)

        except Exception:

            market = {}


        best_setup = {}

        if isinstance(final_smc, dict):
            best_setup = final_smc.get("best_setup", {})


        result["MARKET"] = market

        result["SMART_MONEY"] = final_smc


        result["FINAL_ENGINE"] = final_smc


        result["SIGNAL"] = {

            "direction": best_setup.get("direction"),

            "score": best_setup.get("score", 0),

            "confidence": best_setup.get("score", 0)

        }


        result["ENTRY"] = {

            "price": candles[-1]["close"]

        }


        result["TRADE_PLAN"] = {

            "STATUS": "WAIT",

            "DIRECTION": best_setup.get(
                "direction",
                "NONE"
            ),

            "ENTRY_ZONE": best_setup.get(
                "zone",
                {}
            ),

            "STOP_LOSS": best_setup.get(
                "stop_loss"
            ),

            "TAKE_PROFIT": best_setup.get(
                "take_profit"
            ),

            "RISK_REWARD": 1.5,

            "CONFIDENCE": best_setup.get(
                "score",
                0
            )

        }


        return result
