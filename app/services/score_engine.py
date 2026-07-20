class ScoreEngine:


    def calculate(self, features, reasons, score):


        indicators = features.get(
            "indicators",
            {}
        )


        if not indicators:
            return score, reasons



        # RSI

        rsi = indicators.get(
            "rsi",
            50
        )


        if rsi < 35:

            score += 10

            reasons.append(
                "RSI oversold"
            )


        elif rsi > 65:

            score += 5

            reasons.append(
                "RSI momentum"



            )



        # TREND EMA

        if indicators.get("trend") == "BULLISH":

            score += 10

            reasons.append(
                "EMA bullish trend"
            )



        # MACD

        if indicators.get("macd",0) > 0:

            score += 10

            reasons.append(
                "MACD bullish"
            )



        # VOLUME

        if indicators.get("volume_ratio",0) > 2:

            score += 15

            reasons.append(
                "Volume spike"
            )



        # MOMENTUM

        if indicators.get("momentum",0) > 0:

            score += 5

            reasons.append(
                "Momentum positive"
            )



        if score > 100:

            score = 100



        return score, reasons
