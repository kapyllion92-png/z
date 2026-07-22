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
        print(
            result.get("features")
        )


        print()
        print("SMART MONEY:")

        smart = result.get(
            "smart_money",
            result
        )

        print(smart)


        print()
        print("CHoCH:")

        print(
            smart.get(
                "choch"
            )
        )


        print()
        print("BOS:")

        print(
            smart.get(
                "bos"
            )
        )


        print()
        print("SIGNAL:")

        signal = smart.get(
            "SIGNAL",
            {}
        )

        print(
            f"{signal.get('direction')} | "
            f"SCORE {signal.get('score')} | "
            f"CONFIDENCE {signal.get('confidence')}"
        )


        print()
        print("ENTRY:")

        print(
            smart.get(
                "ENTRY"
            )
        )


        print()
        print("TRADE PLAN:")

        plan = smart.get(
            "TRADE_PLAN",
            {}
        )

        print(
f"""
STATUS: {plan.get('STATUS')}
DIRECTION: {plan.get('DIRECTION')}
ENTRY ZONE: {plan.get('ENTRY_ZONE')}
STOP LOSS: {plan.get('STOP_LOSS')}
TAKE PROFIT: {plan.get('TAKE_PROFIT')}
RISK/REWARD: {plan.get('RISK_REWARD')}
CONFIDENCE: {plan.get('CONFIDENCE')}%
"""
        )


        print("=" * 60)
