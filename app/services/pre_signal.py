from app.services.signal import Signal


class PreSignal:


    def __init__(self):

        pass



    def analyze(self, candles, symbol):


        try:


            if candles is None:

                return None



            if len(candles) < 50:

                return None



            closes = []

            volumes = []



            for c in candles:


                if len(c) < 6:

                    continue


                closes.append(
                    float(c[4])
                )


                volumes.append(
                    float(c[5])
                )



            if len(closes) < 50:

                return None




            price = closes[-1]

            old_price = closes[-20]



            change = (

                (price-old_price)

                /

                old_price

                *

                100

            )




            avg_volume = sum(

                volumes[-20:]

            ) / 20




            volume_power = (

                volumes[-1]

                >

                avg_volume * 1.3

            )



            # простой RSI


            gains = []

            losses = []



            for i in range(

                1,

                len(closes)

            ):


                diff = closes[i] - closes[i-1]


                if diff >= 0:

                    gains.append(diff)

                    losses.append(0)


                else:

                    gains.append(0)

                    losses.append(abs(diff))





            avg_gain = sum(

                gains[-14:]

            ) / 14



            avg_loss = sum(

                losses[-14:]

            ) / 14




            if avg_loss == 0:

                rsi = 100


            else:


                rs = avg_gain / avg_loss


                rsi = 100 - (

                    100 /

                    (1 + rs)

                )





            reasons = []

            strength = 0



            direction = None

            strategy = ""





            # Отскок после дампа


            if change <= -1:


                direction = "LONG"


                strategy = (

                    "Отскок после дампа"

                )


                strength += 30


                reasons.append(

                    "Цена упала более 1%"

                )




                if volume_power:


                    strength += 20


                    reasons.append(

                        "Повышенный объём"

                    )





                if rsi < 40:


                    strength += 20


                    reasons.append(

                        "RSI показывает перепроданность"

                    )





            # Отскок после пампа


            if change >= 1:


                direction = "SHORT"


                strategy = (

                    "Отскок после пампа"

                )


                strength += 30


                reasons.append(

                    "Цена выросла более 1%"

                )




                if volume_power:


                    strength += 20


                    reasons.append(

                        "Высокий объём"

                    )




                if rsi > 60:


                    strength += 20


                    reasons.append(

                        "RSI показывает перекупленность"

                    )





            if direction is None:

                return None





            entry = price



            stop = (

                price * 0.995

                if direction=="LONG"

                else

                price * 1.005

            )



            target = (

                price * 1.03

                if direction=="LONG"

                else

                price * 0.97

            )





            return {


                "монета":

                symbol,


                "направление":

                direction,


                "стратегия":

                strategy,


                "сила":

                min(

                    strength,

                    100

                ),


                "причины":

                reasons,


                "вход":

                round(

                    entry,

                    4

                ),


                "стоп":

                round(

                    stop,

                    4

                ),


                "тейк":

                round(

                    target,

                    4

                ),


                "доходность":

                "3%"


            }





        except Exception as e:


            print(

                "PreSignal internal error",

                symbol,

                e

            )


            return None
