class RangeBreakStrategy:

    def analyze(self, features):

        closes = features.get(
            "closes",
            []
        )

        volumes = features.get(
            "volumes",
            []
        )


        score = 0
        reasons = []


        if len(closes) < 30:

            return {

                "strategy":"RANGE_BREAK",

                "signal":"NONE",

                "score":0,

                "reasons":[
                    "NOT ENOUGH DATA"
                ]
            }



        recent = closes[-20:]


        high = max(recent)

        low = min(recent)


        range_size = (
            high - low
        ) / low



        # проверяем сжатие

        if range_size < 0.015:

            score += 25

            reasons.append(
                "TIGHT RANGE +25"
            )



        current = closes[-1]



        signal = "NONE"



        # выход вверх

        if current > high * 0.998:

            score += 30

            reasons.append(
                "RANGE BREAK UP +30"
            )

            signal = "LONG"



        # выход вниз

        elif current < low * 1.002:

            score += 30

            reasons.append(
                "RANGE BREAK DOWN +30"
            )

            signal = "SHORT"



        # объём подтверждает

        if len(volumes) >= 20:

            avg_volume = sum(
                volumes[-20:]
            ) / 20


            if volumes[-1] > avg_volume:

                score += 20

                reasons.append(
                    "VOLUME CONFIRM +20"
                )



        if score < 40:

            signal = "NONE"



        return {

            "strategy":
                "RANGE_BREAK",

            "signal":
                signal,

            "score":
                score,

            "reasons":
                reasons
        }
