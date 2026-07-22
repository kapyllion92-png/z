from app.services.historical.database import HistoricalDatabase
from app.services.smart_money.liquidity_engine import LiquidityEngine


print("START LIQUIDITY TEST")


db = HistoricalDatabase()

engine = LiquidityEngine()


symbol = "BTCUSDT"


candles = db.get_candles(
    symbol,
    "60",
    100
)


print("SYMBOL:", symbol)

print("CANDLES:", len(candles))


result = engine.analyze(candles)



print("\n===== LIQUIDITY RESULT =====")


print("EQUAL HIGHS:",
      result["equal_highs"])


print("EQUAL LOWS:",
      result["equal_lows"])


print("LIQUIDITY SWEEP:",
      result["liquidity_sweep"])


print("LIQUIDITY GRAB:",
      result["liquidity_grab"])


print("STOP RUN:",
      result["stop_run"])


print("STOP HUNT:",
      result["stop_hunt"])


print("RETURN AFTER SWEEP:",
      result["return_after_sweep"])



print("\nSCORE:",
      result["score"])



print("\nREASONS:")

for r in result["reasons"]:

    print("-", r)



print("\nLIQUIDITY TEST OK")
