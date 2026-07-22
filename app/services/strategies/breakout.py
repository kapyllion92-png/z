class BreakoutStrategy:

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

                "strategy":"BREAKOUT",

                "signal":"NONE",

                "score":0,

                "reasons":[
                    "NOT ENOUGH DATA"
                ]
            }



        # диапазон последних свечей

        high_range = max(
            closes[-20:]
        )

        low_range = min(
            closes[-20:]
        )


        # пробой вверх

        if close > high_range * 0.998:

            score += 25

            reasons.append(
                "BREAK HIGH +25"
            )


        # пробой вниз

        elif close < low_range * 1.002:

            score += 25

            reasons.append(
                "BREAK LOW +25"
            )



        # проверяем объём

        if len(volumes) >= 20:

            avg_volume = sum(
                volumes[-20:]
            ) / 20


            if volumes[-1] > avg_volume:

                score += 20

                reasons.append(
                    "VOLUME CONFIRM +20"
                )



        if score >= 40:

            signal = "BREAKOUT"

        else:

            signal = "NONE"



        return {

            "strategy":
                "BREAKOUT",

            "signal":
                signal,

            "score":
                score,

            "reasons":
                reasons
        }
