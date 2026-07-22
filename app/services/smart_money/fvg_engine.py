def _num(v):
    try:
        return float(v)
    except:
        return 0.0


def _get(c,key):

    if isinstance(c,dict):
        return _num(c.get(key,0))

    idx={
        "open":1,
        "high":2,
        "low":3,
        "close":4,
        "volume":5
    }

    try:
        return _num(c[idx[key]])
    except:
        return 0



def fvg_engine_v4000(candles):

    fvgs=[]

    volumes=[
        _get(c,"volume")
        for c in candles
    ]

    avg_volume=sum(volumes)/len(volumes) if volumes else 0



    for i in range(len(candles)-3):

        c1=candles[i]
        c2=candles[i+1]
        c3=candles[i+2]


        h1=_get(c1,"high")
        l1=_get(c1,"low")

        h3=_get(c3,"high")
        l3=_get(c3,"low")

        v2=_get(c2,"volume")


        volume_ratio = (
            v2/avg_volume
            if avg_volume
            else 1
        )


        # bullish FVG

        if l3 > h1:

            gap=[round(h1,4),round(l3,4)]

            score=70

            reasons=[
                "BULLISH FVG",
                "PRICE IMBALANCE"
            ]


            if volume_ratio > 1.1:
                score+=10
                reasons.append(
                    "VOLUME CONFIRMATION"
                )


            if abs(_get(c2,"close")-_get(c2,"open")) > (
                (_get(c2,"high")-_get(c2,"low"))*0.5
            ):
                score+=10
                reasons.append(
                    "DISPLACEMENT CANDLE"
                )


            fvgs.append({

                "event":
                "BULLISH FVG INSTITUTIONAL v4000",

                "type":
                "SMART MONEY FAIR VALUE GAP",

                "direction":
                "LONG",

                "zone":
                gap,

                "score":
                min(score,100),

                "confidence":
                min(score,100),

                "quality":
                (
                "A+ INSTITUTIONAL PREMIUM"
                if score>=90
                else
                "A INSTITUTIONAL"
                if score>=80
                else
                "B QUALITY"
                ),

                "fresh":
                True,

                "status":
                "ACTIVE",

                "reasons":
                reasons
            })



        # bearish FVG

        if h3 < l1:


            gap=[
                round(h3,4),
                round(l1,4)
            ]


            score=70

            reasons=[
                "BEARISH FVG",
                "PRICE IMBALANCE"
            ]


            if volume_ratio > 1.1:
                score+=10
                reasons.append(
                    "VOLUME CONFIRMATION"
                )


            if abs(_get(c2,"close")-_get(c2,"open")) > (
                (_get(c2,"high")-_get(c2,"low"))*0.5
            ):
                score+=10
                reasons.append(
                    "DISPLACEMENT CANDLE"
                )


            fvgs.append({

                "event":
                "BEARISH FVG INSTITUTIONAL v4000",

                "type":
                "SMART MONEY FAIR VALUE GAP",

                "direction":
                "SHORT",

                "zone":
                gap,

                "score":
                min(score,100),

                "confidence":
                min(score,100),

                "quality":
                (
                "A+ INSTITUTIONAL PREMIUM"
                if score>=90
                else
                "A INSTITUTIONAL"
                if score>=80
                else
                "B QUALITY"
                ),

                "fresh":
                True,

                "status":
                "ACTIVE",

                "reasons":
                reasons
            })



    return {

        "tested_candles":
        len(candles),

        "fvg_found":
        len(fvgs),

        "institutional_fvg":
        len(
            [
            f for f in fvgs
            if "INSTITUTIONAL" in f["quality"]
            ]
        ),

        "average_confidence":
        round(
            sum(
                f["confidence"]
                for f in fvgs
            )/len(fvgs),
            2
        )
        if fvgs else 0,

        "top_fvg":
        fvgs[:10]
    }
