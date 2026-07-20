class ScoreEngine:


    def calculate(
        self,
        features,
        structure=None,
        pattern=0
    ):

        score = 50
        reasons = []


        rsi = features.get("rsi",50)
        macd = features.get("macd",0)
        trend = features.get("trend","")
        momentum = features.get("momentum",0)
        volume = features.get("volume_ratio",0)



        # RSI

        if rsi < 20:

            score -= 25

            reasons.append(
                "RSI extreme oversold - риск отскока"
            )

        elif rsi < 30:

            score -= 10

            reasons.append(
                "RSI oversold"
            )

        elif rsi > 80:

            score -= 25

            reasons.append(
                "RSI extreme overbought"
            )

        elif rsi > 70:

            score -= 10

            reasons.append(
                "RSI overbought"
            )



        # MACD

        if macd < 0:

            score += 15

            reasons.append(
                "MACD bearish"
            )

        else:

            score += 15

            reasons.append(
                "MACD bullish"
            )



        # TREND

        if trend == "BEARISH":

            score += 15

            reasons.append(
                "EMA bearish"
            )


        elif trend == "BULLISH":

            score += 15

            reasons.append(
                "EMA bullish"
            )



        # MOMENTUM

        if momentum < 0:

            score += 10

            reasons.append(
                "Momentum bearish"
            )

        else:

            score += 10

            reasons.append(
                "Momentum bullish"
            )



        # VOLUME

        if volume > 1.5:

            score += 5

            reasons.append(
                "Volume confirmation"
            )



        score = max(
            0,
            min(
                score,
                100
            )
        )



        # SIGNAL

        if trend == "BEARISH" and macd < 0:

            signal = "SHORT"

        elif trend == "BULLISH" and macd > 0:

            signal = "LONG"

        else:

            signal = "WAIT"



        confidence = score



        if confidence >= 80:

            status = "READY"

        elif confidence >= 60:

            status = "WATCH"

        else:

            status = "NO_TRADE"



        if rsi < 20:

            status = "WATCH"



        return {

            "signal": signal,

            "score": score,

            "confidence": confidence,

            "status": status,

            "reasons": reasons

        }
