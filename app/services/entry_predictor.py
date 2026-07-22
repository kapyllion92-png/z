from datetime import datetime


class EntryPredictor:


    def predict(self, features, strategy):

        price = float(features.get("close",0))

        atr = float(
            features.get(
                "atr",
                price*0.01
            )
        )

        trend = features.get(
            "trend",
            "UNKNOWN"
        )

        macd = features.get(
            "macd",
            0
        )


        signal = strategy.get(
            "signal",
            "WAIT"
        )


        score = int(
            strategy.get(
                "score",
                0
            )
        )


        reasons = list(
            strategy.get(
                "reasons",
                []
            )
        )


        final_engine = strategy.get(
            "FINAL_ENGINE",
            {}
        )


        best_setup = {}

        if isinstance(final_engine,dict):

            best_setup = final_engine.get(
                "best_setup",
                {}
            )


        # ==========================
        # ORDER BLOCK ENTRY LOGIC
        # ==========================

        if best_setup.get("zone"):

            zone_from = float(
                best_setup["zone"][0]
            )

            zone_to = float(
                best_setup["zone"][1]
            )


            direction = best_setup.get(
                "direction",
                signal
            )


            entry_from = zone_from
            entry_to = zone_to


            inside_zone = (
                zone_from <= price <= zone_to
            )


            if inside_zone:

                status = "READY"

            else:

                status = "WAIT"


            if direction == "LONG":

                stop = zone_from - atr*2

                target = zone_to + atr*3


            else:

                stop = zone_to + atr*2

                target = zone_from - atr*3



            confidence = min(
                100,
                max(
                    score,
                    best_setup.get(
                        "score",
                        0
                    )
                )
            )


            reasons.extend(
                best_setup.get(
                    "reasons",
                    []
                )
            )


            return {

                "status":status,

                "direction":direction,


                "confidence":confidence,


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
                    list(set(reasons)),


                "created":
                    datetime.now().strftime(
                        "%H:%M:%S"
                    )

            }



        # ==========================
        # FALLBACK WITHOUT OB
        # ==========================


        if signal=="LONG":

            entry_from = price-atr*0.3

            entry_to = price+atr*0.2

            stop = price-atr*2

            target = price+atr*3


        elif signal=="SHORT":

            entry_from = price-atr*0.2

            entry_to = price+atr*0.3

            stop = price+atr*2

            target = price-atr*3


        else:

            entry_from=price

            entry_to=price

            stop=0

            target=0



        confidence=min(
            100,
            score
        )


        status="READY" if confidence>=75 else "WAIT"



        return {

            "status":status,

            "direction":signal,

            "confidence":confidence,

            "time_window":"10-15 minutes",

            "entry_zone":
            {
                "from":round(entry_from,2),
                "to":round(entry_to,2)
            },

            "stop_loss":round(stop,2),

            "take_profit":round(target,2),

            "risk_reward":1.5,

            "reasons":list(set(reasons)),

            "created":
                datetime.now().strftime(
                    "%H:%M:%S"
                )

        }
