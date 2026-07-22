class TradeRanker:


    def __init__(self):

        pass



    def calculate_strength(self, data):


        score = 0

        reasons = []



        trend = data.get(
            "trend",
            ""
        )


        rsi = data.get(
            "rsi",
            50
        )


        volume = data.get(
            "volume_power",
            False
        )


        liquidity = data.get(
            "liquidity",
            False
        )


        setup = data.get(
            "strategy",
            ""
        )



        if trend in [
            "STRONG_BULLISH",
            "BULLISH"
        ]:

            score += 15

            reasons.append(
                "Тренд подтверждает LONG"
            )



        if trend in [
            "STRONG_BEARISH",
            "BEARISH"
        ]:

            score += 15

            reasons.append(
                "Тренд подтверждает SHORT"
            )



        if rsi < 35:


            score += 15

            reasons.append(
                "RSI перепроданность"
            )



        if rsi > 65:


            score += 15

            reasons.append(
                "RSI перекупленность"
            )



        if volume:


            score += 20

            reasons.append(
                "Объём выше нормы"
            )



        if liquidity:


            score += 20

            reasons.append(
                "Снятие ликвидности"
            )



        return {

            "сила":

            min(
                score,
                100
            ),


            "причины":

            reasons

        }





    def rank(self, trades):


        result = []



        for trade in trades:


            analysis = self.calculate_strength(
                trade
            )


            trade.update(
                analysis
            )


            result.append(
                trade
            )



        result.sort(

            key=lambda x:

            x.get(
                "сила",
                0
            ),

            reverse=True

        )


        return result[:10]
