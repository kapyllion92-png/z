from datetime import datetime


class CHoCHEngine:


    def __init__(self):

        self.name="CHoCH ENGINE v15.0"



    def analyze(
        self,
        candles,
        volume_ratio=1.0,
        order_blocks=None
    ):


        if not candles or len(candles)<30:

            return {
                "engine":self.name,
                "choch":"NONE",
                "score":0
            }



        highs=[c["high"] for c in candles]
        lows=[c["low"] for c in candles]
        closes=[c["close"] for c in candles]


        current=closes[-1]


        previous_high=max(
            highs[-20:-5]
        )

        previous_low=min(
            lows[-20:-5]
        )



        tolerance=current*0.001



        sweep_high=False
        sweep_low=False


        reclaim_high=False
        reclaim_low=False



        # liquidity sweep

        if max(highs[-5:]) > previous_high:

            sweep_high=True


        if min(lows[-5:]) < previous_low:

            sweep_low=True



        # reclaim

        if sweep_low and current > previous_low:

            reclaim_low=True


        if sweep_high and current < previous_high:

            reclaim_high=True



        displacement=(

            abs(
                closes[-1]-closes[-5]
            )

            >

            abs(
                closes[-10]-closes[-5]
            )

        )



        choch="NONE"

        bos="NONE"

        score=0

        reasons=[]



        # bullish

        if reclaim_low and displacement:

            choch="BULLISH"

            score+=70

            reasons.append(
                "BULLISH LIQUIDITY RECLAIM"
            )


        elif current > previous_high+tolerance:

            bos="BULLISH"

            score+=30

            reasons.append(
                "BREAK HIGH"
            )



        # bearish


        if reclaim_high and displacement:

            choch="BEARISH"

            score+=70

            reasons.append(
                "BEARISH LIQUIDITY RECLAIM"
            )


        elif current < previous_low-tolerance:

            bos="BEARISH"

            score+=30

            reasons.append(
                "BREAK LOW"
            )



        if displacement:

            score+=20
            reasons.append(
                "DISPLACEMENT"
            )



        if order_blocks:

            score+=10
            reasons.append(
                "ORDER BLOCK"
            )



        score=min(score,100)



        return {


            "engine":
                self.name,


            "timestamp":
                str(datetime.now()),


            "choch":
                choch,


            "bos":
                bos,


            "score":
                score,


            "ready":
                (
                choch!="NONE"
                and score>=80
                ),


            "confidence":
                score,


            "levels":{

                "high":
                    previous_high,

                "low":
                    previous_low,

                "current":
                    current

            },


            "debug":{

                "sweep_high":
                    sweep_high,

                "sweep_low":
                    sweep_low,

                "reclaim_high":
                    reclaim_high,

                "reclaim_low":
                    reclaim_low,

                "displacement":
                    displacement

            },


            "reasons":
                reasons

        }



def detect_choch(
    candles,
    volume_ratio=1.0,
    order_blocks=None
):

    return CHoCHEngine().analyze(
        candles,
        volume_ratio,
        order_blocks
    )
