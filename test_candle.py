from app.services.smart_money.candle_engine import CandleEngine


def candle(open_, high, low, close):
    return {
        "open": open_,
        "high": high,
        "low": low,
        "close": close
    }


engine = CandleEngine()


tests = [

    (
        "BULLISH ENGULFING",
        [
            candle(110,115,100,102),
            candle(101,120,99,118)
        ]
    ),

    (
        "HAMMER",
        [
            candle(100,103,90,102),
            candle(101,103,90,102)
        ]
    ),

    (
        "DOJI",
        [
            candle(100,105,95,100.2),
            candle(100,105,95,100.1)
        ]
    ),

    (
        "INSIDE BAR",
        [
            candle(100,110,90,105),
            candle(103,108,95,106)
        ]
    ),

]


print("===== CANDLE PATTERN TEST =====")


for name, candles in tests:

    r = engine.analyze(candles)

    print()
    print(name)

    print(r)

    print("SCORE:", r["score"])
    print("REASONS:", r["reasons"])
