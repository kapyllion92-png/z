def parse_candle(candle):
    return {
        "time": int(candle[0]),
        "open": float(candle[1]),
        "high": float(candle[2]),
        "low": float(candle[3]),
        "close": float(candle[4]),
        "volume": float(candle[5]),
        "turnover": float(candle[6]),
    }


def parse_candles(candles):
    return [parse_candle(candle) for candle in candles]
