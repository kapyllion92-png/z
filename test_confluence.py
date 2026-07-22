from app.services.smart_money_engine import SmartMoneyEngine
from app.services.historical.database import HistoricalDatabase


print("START CONFLUENCE TEST")


db = HistoricalDatabase()

engine = SmartMoneyEngine()


candles = db.get_candles(
    "BTCUSDT",
    "60",
    100
)


print("CANDLES:", len(candles))


result = engine.modular_analysis(
    candles
)


print("\n===== FINAL RESULT =====")


print("DIRECTION:", result.get("direction"))

print("SCORE:", result.get("score"))

print("GRADE:", result.get("grade"))


print("\nREASONS:")

for r in result.get("reasons", []):
    print("-", r)


print("\nCONFLUENCE TEST OK")

