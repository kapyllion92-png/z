from datetime import datetime


class EntryPredictor:


    def predict(self, features, strategy):

        price = float(
            features.get(
                "close",
                0
            )
        )

        rsi = features.get("rsi",50)
        macd = features.get("macd",0)
        trend = features.get("trend","UNKNOWN")
        atr = features.get(
            "atr",
            price * 0.01
        )


        signal = strategy.get(
            "signal",
            "WAIT"
        )


        score = 50
        reasons = []


        if trend == "BEARISH":

            score += 15

            reasons.append(
                "Bearish trend confirmation"
            )


        if trend == "BULLISH":

            score += 15

            reasons.append(
                "Bullish trend confirmation"
            )


        if macd < 0:

            score += 10

            reasons.append(
                "MACD bearish pressure"
            )


        if macd > 0:

            score += 10

            reasons.append(
                "MACD bullish pressure"
            )


        if signal in [
            "LONG",
            "SHORT"
        ]:

            score += 15

            reasons.append(
                "Strategy confirmation"
            )


        confidence = min(
            score,
            95
        )


        if signal == "LONG":

            entry_from = price - atr*0.3
            entry_to = price + atr*0.2

            stop = price - atr*2

            target = price + atr*3


        elif signal == "SHORT":

            entry_from = price - atr*0.2
            entry_to = price + atr*0.3

            stop = price + atr*2

            target = price - atr*3


        else:

            entry_from = price
            entry_to = price

            stop = 0
            target = 0



        if confidence >= 75:

            status="READY"

        elif confidence >=55:

            status="WATCH"

        else:

            status="WAIT"



        return {

            "status": status,

            "direction": signal,

            "confidence": confidence,

            "time_window":
                "10-15 minutes",

            "entry_zone":
            {
                "from":
                    round(entry_from,2),

                "to":
                    round(entry_to,2)
            },


            "stop_loss":
                round(stop,2),


            "take_profit":
                round(target,2),


            "risk_reward":
                1.5,


            "reasons":
                reasons,


            "created":
                datetime.now().strftime(
                    "%H:%M:%S"
                )

        }
