class IndicatorEngine:


    def analyze(self, candles):

        closes = []
        highs = []
        lows = []
        volumes = []


        for c in candles:

            closes.append(float(c["close"]))

            highs.append(
                float(c.get("high", c["close"]))
            )

            lows.append(
                float(c.get("low", c["close"]))
            )

            volumes.append(
                float(c.get("volume",0))
            )


        result = {}


        # SMA

        result["sma20"] = self.sma(closes,20)
        result["sma50"] = self.sma(closes,50)
        result["sma200"] = self.sma(closes,200)



        # EMA

        result["ema20"] = self.ema(closes,20)
        result["ema50"] = self.ema(closes,50)
        result["ema200"] = self.ema(closes,200)



        # RSI

        result["rsi"] = self.rsi(closes)



        # MACD

        result["macd"] = (
            result["ema20"]
            -
            result["ema50"]
        )



        # ATR

        result["atr"] = self.atr(
            highs,
            lows,
            closes
        )



        # Bollinger

        sma20 = result["sma20"]

        if sma20:

            std = (
                sum(
                    [
                    (x-sma20)**2
                    for x in closes[-20:]
                    ]
                )
                /
                20
            ) ** 0.5


            result["bb_upper"] = sma20 + 2*std
            result["bb_lower"] = sma20 - 2*std



        # Volume

        avg_volume = (
            sum(volumes[-20:])
            /
            20
            if len(volumes)>=20
            else 0
        )


        result["volume_ratio"] = (
            volumes[-1]/avg_volume
            if avg_volume
            else 0
        )



        # VWAP

        total = 0
        vol = 0

        for p,v in zip(closes,volumes):

            total += p*v
            vol += v


        result["vwap"] = (
            total/vol
            if vol
            else closes[-1]
        )



        # Momentum

        if len(closes)>10:

            result["momentum"] = (
                closes[-1]-closes[-10]
            )



        # ROC

        if len(closes)>12:

            result["roc"] = (
                (
                closes[-1]
                /
                closes[-12]
                )
                -1
            )*100



        # Williams %R

        high=max(highs[-14:])
        low=min(lows[-14:])


        result["williams_r"] = (
            (
            high-closes[-1]
            )
            /
            (high-low)
            *
            -100
            if high!=low
            else 0
        )


        # Trend


        if (
            result["ema20"]
            >
            result["ema50"]
        ):

            result["trend"]="BULLISH"

        else:

            result["trend"]="BEARISH"



        return result




    def sma(self,data,n):

        if len(data)<n:
            return sum(data)/len(data)

        return sum(data[-n:])/n



    def ema(self,data,n):

        if not data:
            return 0


        k=2/(n+1)

        ema=data[0]


        for price in data[1:]:

            ema = (
                price*k
                +
                ema*(1-k)
            )

        return ema




    def rsi(self,data,n=14):

        if len(data)<n+1:
            return 0


        gains=[]
        losses=[]


        for i in range(1,n+1):

            diff=data[-i]-data[-i-1]


            if diff>=0:

                gains.append(diff)

            else:

                losses.append(abs(diff))


        avg_gain=sum(gains)/n
        avg_loss=sum(losses)/n


        if avg_loss==0:
            return 100


        rs=avg_gain/avg_loss


        return round(
            100-(100/(1+rs)),
            2
        )



    def atr(self,h,l,c,n=14):

        tr=[]


        for i in range(1,len(c)):

            tr.append(
                max(
                    h[i]-l[i],
                    abs(h[i]-c[i-1]),
                    abs(l[i]-c[i-1])
                )
            )


        if len(tr)<n:
            return 0


        return sum(tr[-n:])/n

