class ImbalanceStrategy:

    def analyze(self, features):

        highs = features.get(
            "highs",
            []
        )

        lows = features.get(
            "lows",
            []
        )

        closes = features.get(
            "closes",
            []
        )


        score = 0
        reasons = []


        if len(closes) < 5:

            return {

                "strategy":"IMBALANCE",

                "signal":"NONE",

                "score":0,

                "reasons":[
                    "NOT ENOUGH DATA"
                ]

            }



        current = closes[-1]

        previous = closes[-2]



        # сильное движение вверх

        move_up = (
            current - previous
        ) / previous



        # сильное движение вниз

        move_down = (
            previous - current
        ) / previous



        signal = "NONE"



        # бычий имбаланс

        if move_up > 0.003:

            score += 30

            reasons.append(
                "BULLISH IMBALANCE +30"
            )

            signal = "LONG"



        # медвежий имбаланс

        elif move_down > 0.003:

            score += 30

            reasons.append(
                "BEARISH IMBALANCE +30"
            )

            signal = "SHORT"



        # проверка объёма

        volumes = features.get(
            "volumes",
            []
        )


        if len(volumes) >= 20:

            avg_volume = sum(
                volumes[-20:]
            ) / 20


            if volumes[-1] > avg_volume:

                score += 20

                reasons.append(
                    "IMBALANCE WITH VOLUME +20"
                )



        if score < 30:

            signal = "NONE"



        return {

            "strategy":
                "IMBALANCE",

            "signal":
                signal,

            "score":
                score,

            "reasons":
                reasons
        }
