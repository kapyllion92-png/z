from pathlib import Path

p = Path("app/services/smart_money_engine.py")

text = p.read_text(encoding="utf-8")


if "PremiumDiscountEngine" not in text:

    text = text.replace(
        "from app.services.smart_money.liquidity_engine import LiquidityEngine",
        "from app.services.smart_money.liquidity_engine import LiquidityEngine\nfrom app.services.smart_money.premium_discount_engine import PremiumDiscountEngine"
    )


    text = text.replace(
        "self.liquidity_engine = LiquidityEngine()",
        "self.liquidity_engine = LiquidityEngine()\n        self.premium_discount_engine = PremiumDiscountEngine()"
    )


    text = text.replace(
        "modules['liquidity'] = self.liquidity_engine.analyze(candles)",
        "modules['liquidity'] = self.liquidity_engine.analyze(candles)\n        modules['premium_discount'] = self.premium_discount_engine.analyze(candles)"
    )


    p.write_text(text, encoding="utf-8")


print("PREMIUM DISCOUNT CONNECT PATCH OK")
