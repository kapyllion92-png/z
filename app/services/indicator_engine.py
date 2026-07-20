class IndicatorEngine:


    def rsi(self, closes, period=14):

        if len(closes) < period + 1:
            return 0

        gains = []
        losses = []

        for i in range(1, period + 1):

            diff = closes[-i] - closes[-i-1]

            if diff >= 0:
                gains.append(diff)
            else:
                losses.append(abs(diff))


        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 1


        rs = avg_gain / avg_loss

        return round(
            100 - (100 / (1 + rs)),
            2
        )



    def sma(self, closes, period=20):

        if len(closes) < period:
            return 0

        return round(
            sum(closes[-period:]) / period,
            4
        )



    def ema(self, closes, period=20):

        if len(closes) < period:
            return 0

        multiplier = 2 / (period + 1)

        ema = sum(closes[:period]) / period


        for price in closes[period:]:

            ema = (
                price - ema
            ) * multiplier + ema


        return round(
            ema,
            4
        )



    def atr(self, candles, period=14):

        if len(candles) < period + 1:
            return 0


        trs = []


        for i in range(1, len(candles)):

            high = float(candles[i]["high"])
            low = float(candles[i]["low"])
            prev = float(candles[i-1]["close"])


            tr = max(

                high - low,

                abs(high - prev),

                abs(low - prev)

            )

            trs.append(tr)


        return round(
            sum(trs[-period:]) / period,
            4
        )



    def analyze(self, candles):


        closes = [
            float(c["close"])
            for c in candles
        ]


        result = {


            "rsi":
                self.rsi(closes),


            "sma20":
                self.sma(closes,20),


            "ema20":
                self.ema(closes,20),


            "trend":
                "BULLISH"
                if closes[-1] > self.ema(closes,20)
                else "BEARISH",


            "price":
                closes[-1]


        }


        return result
