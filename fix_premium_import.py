from pathlib import Path

p = Path("app/services/smart_money_engine.py")

text = p.read_text(encoding="utf-8")

# убираем неправильный импорт
text = text.replace(
"from app.services.smart_money.premium_discount_engine import PremiumDiscountEngine\n",
""
)

# вставляем импорт в самое начало файла
if "from app.services.smart_money.premium_discount_engine import PremiumDiscountEngine" not in text:
    lines = text.splitlines()

    insert = 0

    while insert < len(lines) and (
        lines[insert].startswith("from ")
        or lines[insert].startswith("import ")
        or lines[insert].strip() == ""
    ):
        insert += 1

    lines.insert(
        insert,
        "from app.services.smart_money.premium_discount_engine import PremiumDiscountEngine"
    )

    text = "\n".join(lines)


# добавляем инициализацию если нет
if "self.premium_discount_engine" not in text:

    text = text.replace(
        "self.liquidity_engine = LiquidityEngine()",
        "self.liquidity_engine = LiquidityEngine()\n        self.premium_discount_engine = PremiumDiscountEngine()"
    )


# добавляем модуль если нет
if "premium_discount" not in text:

    text = text.replace(
        "modules['liquidity'] = self.liquidity_engine.analyze(candles)",
        "modules['liquidity'] = self.liquidity_engine.analyze(candles)\n        modules['premium_discount'] = self.premium_discount_engine.analyze(candles)"
    )


p.write_text(text, encoding="utf-8")

print("PREMIUM IMPORT FIX OK")
