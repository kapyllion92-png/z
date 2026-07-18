from app.services.indicators.basic import (
    sma,
    ema,
    rsi,
    atr,
)


class FeatureBuilder:


    def build(self, candles):

        closes = [
            candle[7]
            for candle in candles
        ]

        highs = [
            candle[5]
            for candle in candles
        ]

        lows = [
            candle[6]
            for candle in candles
        ]

        volumes = [
            candle[8]
            for candle in candles
        ]


        return {
            "close": closes[-1],
            "volume": volumes[-1],

            "sma": sma(closes),

            "ema": ema(closes),

            "rsi": rsi(closes),

            "atr": atr(
                highs,
                lows,
                closes,
            ),
        }
