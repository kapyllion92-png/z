from app.services.historical.history_loader import HistoryLoader
from app.services.strategy.strategy_engine import StrategyEngine


loader = HistoryLoader()


candles = loader.load(
    "SOLUSDT",
    "15"
)


engine = StrategyEngine()


result = engine.analyze(candles)


print("======================")
print("STRATEGY RESULT")
print("======================")


for k,v in result.items():

    print(k,":",v)