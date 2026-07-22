class ScoreEngine:

    def calculate(
        self,
        features,
        smart_money=None,
        confidence=0
    ):

        score = 0
        reasons = []


        if not isinstance(smart_money, dict):
            smart_money = {}


        if not isinstance(features, dict):
            features = {}


        # RSI

        rsi = features.get(
            "rsi",
            50
        )

        if rsi < 30:

            score += 10

            reasons.append(
                "RSI OVERSOLD"
            )


        elif rsi > 70:

            score += 10

            reasons.append(
                "RSI OVERBOUGHT"
            )


        # TREND

        trend = features.get(
            "trend",
            ""
        )


        if trend == "BEARISH":

            score += 10

            reasons.append(
                "BEARISH TREND"
            )


        elif trend == "BULLISH":

            score += 10

            reasons.append(
                "BULLISH TREND"
            )


        # SMART MONEY

        sm_score = smart_money.get(
            "score",
            0
        )


        if isinstance(sm_score,(int,float)):

            score += min(
                int(sm_score),
                30
            )


            if sm_score > 0:

                reasons.append(
                    "SMART MONEY"
                )


        # CONFIDENCE

        if confidence >= 85:

            score += 10

            reasons.append(
                "HIGH CONFIDENCE"
            )


        score=min(
            100,
            score
        )


        if score >=85:

            grade="A+"

        elif score>=70:

            grade="A"

        elif score>=55:

            grade="B"

        else:

            grade="LOW"


        return {

            "score":score,

            "confidence":confidence,

            "grade":grade,

            "reasons":reasons

        }
