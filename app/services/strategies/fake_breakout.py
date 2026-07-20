class FakeBreakoutStrategy:

    def analyze(self, features):

        closes = features.get(
            "closes",
            []
        )

        volumes = features.get(
            "volumes",
            []
        )

        close = features["close"]


        score = 0
        reasons = []


        if len(closes) < 20:

            return {

                "strategy":"FAKE_BREAKOUT",

                "signal":"NONE",

                "score":0,

                "reasons":[
                    "NOT ENOUGH DATA"
                ]
            }



        previous_high = max(
            closes[-20:-1]
        )

        previous_low = min(
            closes[-20:-1]
        )



        # ложный пробой вверх
        # вышли выше уровня и вернулись назад

        if max(closes[-3:]) > previous_high and close < previous_high:

            score += 30

            reasons.append(
                "FAILED HIGH BREAK +30"
            )


            signal = "SHORT"



        # ложный пробой вниз

        elif min(closes[-3:]) < previous_low and close > previous_low:

            score += 30

            reasons.append(
                "FAILED LOW BREAK +30"
            )


            signal = "LONG"



        else:

            signal = "NONE"



        # подтверждение объёмом

        if len(volumes) >= 20:

            avg_volume = sum(
                volumes[-20:]
            ) / 20


            if volumes[-1] > avg_volume:

                score += 20

                reasons.append(
                    "VOLUME CONFIRM +20"
                )



        if score < 30:

            signal = "NONE"



        return {

            "strategy":
                "FAKE_BREAKOUT",

            "signal":
                signal,

            "score":
                score,

            "reasons":
                reasons
        }
