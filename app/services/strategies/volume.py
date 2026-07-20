class VolumeStrategy:

    def analyze(self, features):

        volumes = features.get(
            "volumes",
            []
        )

        closes = features.get(
            "closes",
            []
        )

        score = 0
        reasons = []


        if len(volumes) < 20 or len(closes) < 20:

            return {

                "strategy":"VOLUME",

                "signal":"NONE",

                "score":0,

                "reasons":[
                    "NOT ENOUGH DATA"
                ]
            }



        current_volume = volumes[-1]


        avg_volume = sum(
            volumes[-20:]
        ) / 20



        volume_ratio = (
            current_volume / avg_volume
            if avg_volume > 0
            else 0
        )



        # сильный объём

        if volume_ratio > 2:

            score += 35

            reasons.append(
                "VOLUME SPIKE x2 +35"
            )


        elif volume_ratio > 1.5:

            score += 20

            reasons.append(
                "HIGH VOLUME +20"
            )



        # направление движения

        price_change = (
            closes[-1] - closes[-2]
        )


        if price_change > 0:

            score += 10

            reasons.append(
                "BUY PRESSURE +10"
            )


            signal = "LONG"


        elif price_change < 0:

            score += 10

            reasons.append(
                "SELL PRESSURE +10"
            )


            signal = "SHORT"


        else:

            signal = "NONE"



        if score < 30:

            signal = "NONE"



        return {

            "strategy":
                "VOLUME",

            "signal":
                signal,

            "score":
                score,

            "reasons":
                reasons,

            "volume_ratio":
                round(volume_ratio,2)

        }
