class SignalScorer:


    def score(self, features, analysis):

        score = 0
        reasons = []
        warnings = []


        # Trend

        if analysis["trend"] == "BULLISH":

            score += 30

            reasons.append(
                "Bullish trend"
            )


        elif analysis["trend"] == "BEARISH":

            score += 30

            reasons.append(
                "Bearish trend"
            )


        else:

            warnings.append(
                "No clear trend"
            )



        # RSI

        rsi = features["rsi"]


        if 40 <= rsi <= 60:

            score += 20

            reasons.append(
                "Healthy RSI"
            )


        elif rsi < 30:

            warnings.append(
                "Oversold"
            )


        elif rsi > 70:

            warnings.append(
                "Overbought"
            )



        # ATR volatility

        atr = features["atr"]


        if atr:

            score += 20

            reasons.append(
                "Volatility available"
            )



        # Volume

        if features["volume"] > 0:

            score += 10

            reasons.append(
                "Volume data available"
            )



        return {

            "score": min(score, 100),

            "signal": analysis["signal"],

            "reasons": reasons,

            "warnings": warnings,

        }
