from pathlib import Path

p = Path("app/services/smart_money_engine.py")

text = p.read_text(encoding="utf-8")

if "LiquidityEngine" not in text:

    text = text.replace(
        "from typing import",
        "from app.services.smart_money.liquidity_engine import LiquidityEngine\n\nfrom typing import"
    )

    text = text.replace(
        "class SmartMoneyEngine:",
        "class SmartMoneyEngine:\n\n    def __init__(self):\n        self.liquidity_engine = LiquidityEngine()"
    )

    text = text.replace(
        "modules = {}",
        "modules = {}\n\n        modules['liquidity'] = self.liquidity_engine.analyze(candles)"
    )

    p.write_text(text, encoding="utf-8")

print("LIQUIDITY ENGINE CONNECT PATCH OK")
