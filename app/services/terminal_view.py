from datetime import datetime


class TerminalView:

    def show_report(self, result):

        print()
        print("=" * 60)
        print("BYBIT PRO TERMINAL X")
        print(datetime.now())
        print("=" * 60)

        print()
        print("MARKET:")
        print(result.get("features"))

        print()
        print("SMART MONEY:")
        print(result.get("smart_money"))

        print()
        print("SIGNAL:")
        strategy = result.get("strategy", {})
        print(
            f"{strategy.get('signal')} | "
            f"SCORE {strategy.get('score')} | "
            f"CONFIDENCE {strategy.get('confidence')}"
        )

        print()
        print("ENTRY:")
        print(result.get("entry"))

        print()
        print("TRADE PLAN:")
        plan = result.get("trade_plan", {})

        print(
            f"""
STATUS: {plan.get('status')}
DIRECTION: {plan.get('direction')}
ENTRY ZONE: {plan.get('entry_zone')}
STOP LOSS: {plan.get('stop_loss')}
TAKE PROFIT: {plan.get('take_profit')}
RISK/REWARD: {plan.get('risk_reward')}
CONFIDENCE: {plan.get('confidence')}%
"""
        )

        print("=" * 60)
