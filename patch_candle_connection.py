from pathlib import Path

p = Path("app/services/smart_money_engine.py")

s = p.read_text(encoding="utf-8")


# импорт Candle Engine
if "from app.services.smart_money.candle_engine import CandleEngine" not in s:
    s = s.replace(
        "from app.services.smart_money.volatility_engine import VolatilityEngine",
        "from app.services.smart_money.volatility_engine import VolatilityEngine\nfrom app.services.smart_money.candle_engine import CandleEngine"
    )


# создание объекта
if "self.candle = CandleEngine()" not in s:
    s = s.replace(
        "self.volume = VolumeEngine()",
        "self.volume = VolumeEngine()\n        self.candle = CandleEngine()"
    )


# подключение модуля
if "modules['candle']" not in s:
    s = s.replace(
        "modules['volatility'] = self.volatility.analyze(\n            candles\n        )",
        "modules['volatility'] = self.volatility.analyze(\n            candles\n        )\n\n        modules['candle'] = self.candle.analyze(\n            candles\n        )"
    )


p.write_text(s, encoding="utf-8")

print("CANDLE CONNECTION V2 PATCH OK")
