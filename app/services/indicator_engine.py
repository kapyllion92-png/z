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



        result["trend"] = (

            "BULLISH"

            if result["ema20"] > result["ema50"]

            else "BEARISH"

        )


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