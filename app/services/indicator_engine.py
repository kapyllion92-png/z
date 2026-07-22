class IndicatorEngine:


    def analyze(self, candles):

        closes = []
        highs = []
        lows = []
        volumes = []


        for c in candles:

            if isinstance(c, dict):

                closes.append(float(c["close"]))
                highs.append(float(c.get("high", c["close"])))
                lows.append(float(c.get("low", c["close"])))
                volumes.append(float(c.get("volume", 0)))

            else:

                closes.append(float(c[4]))
                highs.append(float(c[2]))
                lows.append(float(c[3]))
                volumes.append(float(c[5]))



        result = {}


        result["sma20"] = self.sma(closes,20)
        result["sma50"] = self.sma(closes,50)
        result["sma200"] = self.sma(closes,200)


        result["ema20"] = self.ema(closes,20)
        result["ema50"] = self.ema(closes,50)
        result["ema200"] = self.ema(closes,200)


        result["rsi"] = self.rsi(closes)


        result["macd"] = (
            result["ema20"]
            -
            result["ema50"]
        )


        result["atr"] = self.atr(
            highs,
            lows,
            closes
        )


        avg_volume = (
            sum(volumes[-20:]) / 20
            if len(volumes) >= 20
            else 0
        )


        result["volume_ratio"] = (

            volumes[-1] / avg_volume

            if avg_volume

            else 0

        )


        result["vwap"] = self.vwap(
            closes,
            volumes
        )


        result["momentum"] = (

            closes[-1] - closes[-10]

            if len(closes) > 10

            else 0

        )


        result["roc"] = (

            (
                closes[-1] / closes[-12]
                - 1
            ) * 100

            if len(closes) > 12

            else 0

        )


        high = max(highs[-14:])
        low = min(lows[-14:])


        result["williams_r"] = (

            (
                (high - closes[-1])
                /
                (high-low)
                *
                -100
            )

            if high != low

            else 0

        )



        result["adx"] = self.adx(candles)

        result["bollinger_bands"] = self.bollinger_bands(candles)

        result["cci"] = self.cci(candles)

        result["donchian_channel"] = self.donchian_channel(candles)

        result["ichimoku"] = self.ichimoku(candles)

        result["keltner_channel"] = self.keltner_channel(candles)

        result["obv"] = self.obv(candles)

        result["parabolic_sar"] = self.parabolic_sar(candles)

        result["stochastic_rsi"] = self.stochastic_rsi(candles)

        result["mfi"] = self.mfi(candles)

        result["supertrend"] = self.supertrend(candles)

        result["trend"] = (

            "BULLISH"

            if result["ema20"] > result["ema50"]

            else "BEARISH"

        )


        indicator_score = 0

        if result.get("rsi",50) < 30:
            indicator_score += 5

        if result.get("rsi",50) > 70:
            indicator_score -= 5

        if result.get("macd",0) > 0:
            indicator_score += 5
        else:
            indicator_score -= 5

        if result.get("adx",0) > 25:
            indicator_score += 5

        if result.get("supertrend",""):
            indicator_score += 5

        if result.get("volume_ratio",0) > 1:
            indicator_score += 5

        result["indicator_score"] = indicator_score

        return result




    def sma(self,data,n):

        if len(data) < n:

            return sum(data)/len(data)

        return sum(data[-n:])/n




    def ema(self,data,n):

        k = 2/(n+1)

        value = data[0]


        for price in data[1:]:

            value = price*k + value*(1-k)


        return value




    def rsi(self,data,n=14):

        if len(data)<=n:

            return 0


        gains = []
        losses = []


        for i in range(1,n+1):

            diff = data[-i]-data[-i-1]


            if diff > 0:

                gains.append(diff)

            else:

                losses.append(abs(diff))


        avg_gain = sum(gains)/n
        avg_loss = sum(losses)/n


        if avg_loss == 0:

            return 100


        rs = avg_gain/avg_loss


        return round(
            100-(100/(1+rs)),
            2
        )




    def atr(self,h,l,c,n=14):

        tr=[]


        for i in range(1,len(c)):

            value=max(
                h[i]-l[i],
                abs(h[i]-c[i-1]),
                abs(l[i]-c[i-1])
            )


            tr.append(value)


        if len(tr)<n:

            return 0


        return sum(tr[-n:])/n




    def vwap(self,prices,volumes):

        total=0
        vol=0


        for p,v in zip(prices,volumes):

            total += p*v
            vol += v


        if vol == 0:

            return prices[-1]


        return total/vol
    def adx(self, candles, period=14):
        try:
            if len(candles) < period + 2:
                return 0

            trs=[]
            plus_dm=[]
            minus_dm=[]

            for i in range(1,len(candles)):

                high=float(candles[i]["high"])
                low=float(candles[i]["low"])

                prev_high=float(candles[i-1]["high"])
                prev_low=float(candles[i-1]["low"])

                tr=max(
                    high-low,
                    abs(high-prev_high),
                    abs(low-prev_low)
                )

                up=high-prev_high
                down=prev_low-low

                trs.append(tr)

                plus_dm.append(
                    up if up>down and up>0 else 0
                )

                minus_dm.append(
                    down if down>up and down>0 else 0
                )


            atr=sum(trs[-period:])/period

            plus=sum(plus_dm[-period:])/atr
            minus=sum(minus_dm[-period:])/atr


            dx=abs(plus-minus)/(plus+minus)*100 if plus+minus else 0

            return round(dx,2)


        except Exception:
            return 0



    def bollinger_bands(self,candles,period=20,mult=2):

        try:

            closes=[
                float(x["close"])
                for x in candles[-period:]
            ]

            if len(closes)<period:
                return {}


            mean=sum(closes)/period


            variance=sum(
                (x-mean)**2
                for x in closes
            )/period


            std=variance**0.5


            return {

                "middle":round(mean,2),

                "upper":round(
                    mean+std*mult,
                    2
                ),

                "lower":round(
                    mean-std*mult,
                    2
                )

            }


        except Exception:
            return {}



    def stochastic_rsi(self,candles,period=14):

        try:

            closes=[
                float(x["close"])
                for x in candles
            ]

            gains=[]
            losses=[]


            for i in range(1,len(closes)):

                diff=closes[i]-closes[i-1]

                gains.append(
                    max(diff,0)
                )

                losses.append(
                    max(-diff,0)
                )


            avg_gain=sum(
                gains[-period:]
            )/period


            avg_loss=sum(
                losses[-period:]
            )/period


            if avg_loss==0:
                rsi=100

            else:
                rs=avg_gain/avg_loss
                rsi=100-(100/(1+rs))


            return round(rsi,2)


        except Exception:
            return 0



    def cci(self,candles,period=20):

        try:

            tp=[
                (
                    float(x["high"])
                    +
                    float(x["low"])
                    +
                    float(x["close"])
                )/3

                for x in candles[-period:]
            ]


            mean=sum(tp)/period


            deviation=sum(
                abs(x-mean)
                for x in tp
            )/period


            return round(
                (tp[-1]-mean)/(0.015*deviation),
                2
            )


        except Exception:
            return 0



    def obv(self,candles):

        try:

            value=0


            for i in range(1,len(candles)):

                close=float(candles[i]["close"])
                prev=float(candles[i-1]["close"])

                volume=float(
                    candles[i]["volume"]
                )


                if close>prev:
                    value+=volume

                elif close<prev:
                    value-=volume


            return value


        except Exception:
            return 0



    def ichimoku(self,candles):

        try:

            highs=[
                float(x["high"])
                for x in candles
            ]

            lows=[
                float(x["low"])
                for x in candles
            ]


            tenkan=(
                max(highs[-9:])
                +
                min(lows[-9:])
            )/2


            kijun=(
                max(highs[-26:])
                +
                min(lows[-26:])
            )/2


            return {

                "tenkan":round(
                    tenkan,
                    2
                ),

                "kijun":round(
                    kijun,
                    2
                )

            }


        except Exception:
            return {}



    def donchian_channel(self,candles,period=20):

        try:

            highs=[
                float(x["high"])
                for x in candles[-period:]
            ]

            lows=[
                float(x["low"])
                for x in candles[-period:]
            ]


            return {

                "upper":max(highs),

                "lower":min(lows),

                "middle":
                    (max(highs)+min(lows))/2

            }


        except Exception:
            return {}



    def keltner_channel(self,candles,period=20):

        try:

            closes=[
                float(x["close"])
                for x in candles[-period:]
            ]

            mean=sum(closes)/period


            return {

                "upper":
                    round(mean*1.02,2),

                "lower":
                    round(mean*0.98,2)

            }


        except Exception:
            return {}



    def parabolic_sar(self,candles):

        try:

            lows=[
                float(x["low"])
                for x in candles[-5:]
            ]

            highs=[
                float(x["high"])
                for x in candles[-5:]
            ]


            return {

                "sar":
                    round(
                        (max(highs)+min(lows))/2,
                        2
                    )

            }


        except Exception:
            return {}


    def macd(self, candles):
        try:
            closes=[float(x["close"]) for x in candles]

            if len(closes)<35:
                return 0

            ema12=sum(closes[-12:])/12
            ema26=sum(closes[-26:])/26

            return ema12-ema26

        except Exception:
            return 0


    def momentum(self, candles, period=10):
        try:
            closes=[float(x["close"]) for x in candles]

            if len(closes)<=period:
                return 0

            return closes[-1]-closes[-period-1]

        except Exception:
            return 0


    def roc(self, candles, period=12):
        try:
            closes=[float(x["close"]) for x in candles]

            if len(closes)<=period:
                return 0

            return (
                (closes[-1]-closes[-period-1])
                /
                closes[-period-1]
            )*100

        except Exception:
            return 0


    def williams_r(self, candles, period=14):
        try:
            highs=[
                float(x["high"])
                for x in candles[-period:]
            ]

            lows=[
                float(x["low"])
                for x in candles[-period:]
            ]

            close=float(candles[-1]["close"])

            high=max(highs)
            low=min(lows)

            if high==low:
                return 0

            return (
                (high-close)
                /
                (high-low)
                *
                -100
            )

        except Exception:
            return 0


    def mfi(self, candles, period=14):
        try:
            positive=0
            negative=0

            data=candles[-period:]

            for c in data:

                price=float(c["close"])
                volume=float(c["volume"])

                flow=price*volume

                if float(c["close"])>=float(c["open"]):
                    positive+=flow
                else:
                    negative+=flow


            if negative==0:
                return 100

            return 100-(100/(1+positive/negative))

        except Exception:
            return 0


    def supertrend(self, candles, period=10, multiplier=3):

        try:

            highs=[
                float(x["high"])
                for x in candles[-period:]
            ]

            lows=[
                float(x["low"])
                for x in candles[-period:]
            ]

            close=float(candles[-1]["close"])

            atr=max(highs)-min(lows)

            upper=(max(highs)+min(lows))/2 + multiplier*atr

            lower=(max(highs)+min(lows))/2 - multiplier*atr


            if close>upper:
                return "BULLISH"

            if close<lower:
                return "BEARISH"

            return "NEUTRAL"


        except Exception:
            return "NEUTRAL"




    def score(self, features):

        score = 50
        reasons = []


        # RSI
        rsi = features.get("rsi",50)

        if rsi < 20:
            score += 8
            reasons.append("RSI OVERSOLD +8")

        elif rsi < 30:
            score += 4
            reasons.append("RSI LOW +4")

        elif rsi > 80:
            score -= 8
            reasons.append("RSI OVERBOUGHT -8")


        # MACD
        macd = features.get("macd",0)

        if macd > 0:
            score += 8
            reasons.append("MACD BULLISH +8")

        else:
            score -= 8
            reasons.append("MACD BEARISH -8")


        # ADX
        adx = features.get("adx",0)

        if adx > 40:
            score += 10
            reasons.append("ADX STRONG TREND +10")

        elif adx > 25:
            score += 5
            reasons.append("ADX TREND +5")


        # Trend EMA
        trend = features.get("trend","")

        if trend=="BULLISH":
            score += 8
            reasons.append("EMA BULLISH +8")

        elif trend=="BEARISH":
            score -= 8
            reasons.append("EMA BEARISH -8")


        # Supertrend

        supertrend = features.get("supertrend","")

        if supertrend=="BULLISH":
            score += 6
            reasons.append("SUPERTREND BULLISH +6")

        elif supertrend=="BEARISH":
            score -= 6
            reasons.append("SUPERTREND BEARISH -6")


        # CCI

        cci = features.get("cci",0)

        if cci < -100:
            score += 5
            reasons.append("CCI REVERSAL +5")

        elif cci > 100:
            score -= 5
            reasons.append("CCI HIGH -5")


        # MFI

        mfi = features.get("mfi",50)

        if mfi < 20:
            score += 5
            reasons.append("MFI OVERSOLD +5")

        elif mfi > 80:
            score -= 5
            reasons.append("MFI OVERBOUGHT -5")


        # Williams %

        williams = features.get("williams_r",-50)

        if williams < -80:
            score += 5
            reasons.append("WILLIAMS OVERSOLD +5")

        elif williams > -20:
            score -= 5
            reasons.append("WILLIAMS OVERBOUGHT -5")


        # Momentum

        momentum = features.get("momentum",0)

        if momentum > 0:
            score += 5
            reasons.append("MOMENTUM UP +5")

        else:
            score -= 5
            reasons.append("MOMENTUM DOWN -5")


        # ROC

        roc = features.get("roc",0)

        if roc > 0:
            score += 5
            reasons.append("ROC POSITIVE +5")

        else:
            score -= 5
            reasons.append("ROC NEGATIVE -5")


        score=max(0,min(score,100))


        return {
            "indicator_score": score,
            "reasons": reasons
        }

