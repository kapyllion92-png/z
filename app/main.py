from app.services.market_data.candles import CandleDataEngine
from app.services.market_data.parser import parse_candles


def main():
    engine = CandleDataEngine()

    response = engine.get_candles(
        symbol="BTCUSDT",
        interval="60",
        limit=5,
    )

    raw_candles = response["result"]["list"]

    candles = parse_candles(raw_candles)

    print(candles[0])
