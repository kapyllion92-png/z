class EntryScore:


    def calculate(self, features):


        score = 0
        reasons = []


        signal = features.get(
            "signal",
            "WAIT"
        )


        ema20 = features["ema20"]
        ema50 = features["ema50"]
        ema200 = features["ema200"]



        # EMA FILTER


        if signal == "LONG":


            if ema20 > ema50 > ema200:

                score += 30

                reasons.append(
                    "EMA BULL CONFIRM +30"
                )

            else:

                reasons.append(
                    "EMA BLOCK LONG"
                )



        elif signal == "SHORT":


            if ema20 < ema50 < ema200:

                score += 30

                reasons.append(
                    "EMA BEAR CONFIRM +30"
                )

            else:

                reasons.append(
                    "EMA BLOCK SHORT"
                )



        # RSI


        rsi = features.get(
            "rsi",
            50
        )


        if 45 <= rsi <= 60:

            score += 20

            reasons.append(
                "RSI IDEAL +20"
            )


        elif 35 <= rsi <= 70:

            score += 10

            reasons.append(
                "RSI GOOD +10"
            )



        # VOLUME


        volumes = features.get(
            "volumes",
            []
        )


        if len(volumes) >= 20:


            avg = sum(
                volumes[-20:]
            ) / 20


            if volumes[-1] > avg:

                score += 15

                reasons.append(
                    "HIGH VOLUME +15"
                )



        # ENTRY ZONE


        close = features["close"]

        sma = features["sma"]


        distance = abs(
            close-sma
        )/sma



        if distance < 0.003:


            score += 20

            reasons.append(
                "GOOD ENTRY ZONE +20"
            )


        elif distance < 0.008:


            score += 10

            reasons.append(
                "ENTRY ZONE +10"
            )



        if score >= 80:

            grade="A"

        elif score >=65:

            grade="B"

        elif score>=50:

            grade="C"

        else:

            grade="D"



        return {

            "score":score,

            "grade":grade,

            "reasons":reasons

        }
