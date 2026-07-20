class BounceStrategy:

    def analyze(self, features):

        close = features["close"]
        sma = features["sma"]

        score = 0
        reasons = []

        distance = abs(close - sma) / sma


        # цена рядом со средней зоной
        if distance < 0.005:

            score += 20
            reasons.append(
                "PRICE NEAR LEVEL +20"
            )


        # проверяем RSI

        rsi = features.get(
            "rsi",
            50
        )


        if rsi < 40:

            score += 15
            reasons.append(
                "OVERSOLD BOUNCE +15"
            )


        if rsi > 60:

            score += 15
            reasons.append(
                "OVERBOUGHT REJECTION +15"
            )


        if score >= 30:

            signal = "BOUNCE"

        else:

            signal = "NONE"



        return {

            "strategy":
                "BOUNCE",

            "signal":
                signal,

            "score":
                score,

            "reasons":
                reasons
        }
