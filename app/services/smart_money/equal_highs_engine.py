def _normalize_candles(candles):
    data=[]

    for c in candles:
        if isinstance(c,dict):
            data.append({
                "high":float(c["high"]),
                "low":float(c["low"]),
                "close":float(c["close"]),
                "volume":float(c.get("volume",0))
            })
        else:
            data.append({
                "high":float(c[2]),
                "low":float(c[3]),
                "close":float(c[4]),
                "volume":float(c[5]) if len(c)>5 else 0
            })

    return data



def equal_highs_engine_v1300(candles):

    candles=_normalize_candles(candles)


    swing_highs=[]


    for i in range(3,len(candles)-3):

        h=candles[i]["high"]

        if (
            h>=candles[i-1]["high"] and
            h>=candles[i-2]["high"] and
            h>=candles[i-3]["high"] and
            h>=candles[i+1]["high"] and
            h>=candles[i+2]["high"] and
            h>=candles[i+3]["high"]
        ):
            swing_highs.append(
                {
                    "price":h,
                    "index":i
                }
            )


    clusters=[]

    tolerance=0.0025


    for sh in swing_highs:

        target=None

        for c in clusters:

            if abs(sh["price"]-c["level"])/c["level"] <= tolerance:
                target=c
                break


        if target:

            target["touches"]+=1
            target["levels"].append(sh["price"])
            target["last"]=sh["index"]

        else:

            clusters.append(
                {
                    "level":sh["price"],
                    "touches":1,
                    "levels":[sh["price"]],
                    "first":sh["index"],
                    "last":sh["index"]
                }
            )


    result=[]


    for c in clusters:


        if c["touches"]<3:
            continue


        level=round(
            sum(c["levels"])/len(c["levels"]),
            4
        )


        age=len(candles)-c["first"]


        score=40


        # touches
        score += min(c["touches"]*6,30)


        # age
        if age>100:
            score+=10


        # sweep
        sweep=False

        for candle in candles[c["last"]+1:]:

            if candle["high"]>level:
                sweep=True
                break


        if sweep:
            score+=10


        if c["touches"]>=7:
            score+=5


        # CAP
        if score>95:
            score=95


        if score>=85:
            quality="INSTITUTIONAL PREMIUM"
        elif score>=70:
            quality="INSTITUTIONAL"
        else:
            quality="HIGH"



        reasons=[
            "EQUAL HIGHS LIQUIDITY POOL",
            "MULTIPLE TOUCHES"
        ]


        if c["touches"]>=5:
            reasons.append(
            "STRONG LIQUIDITY CLUSTER"
            )


        if age>50:
            reasons.append(
            "LIQUIDITY AGE CONFIRMATION"
            )


        if sweep:
            reasons.append(
            "LIQUIDITY SWEEP CONFIRMED"
            )


        reasons.append(
            "INSTITUTIONAL SCORE VALIDATION"
        )


        result.append({

            "event":
            "BUY SIDE EQUAL HIGHS INSTITUTIONAL v1300",

            "type":
            "SMART MONEY LIQUIDITY ZONE",

            "level":
            level,

            "touches":
            c["touches"],

            "age":
            age,

            "score":
            score,

            "confidence":
            score,

            "quality":
            quality,

            "status":
            "ACTIVE",

            "reasons":
            reasons
        })


    result.sort(
        key=lambda x:x["score"],
        reverse=True
    )


    top=result[:10]


    return {

        "tested_candles":
        len(candles),

        "swing_highs_found":
        len(swing_highs),

        "equal_highs_final":
        len(result),

        "institutional_clusters":
        len(
            [x for x in result if x["score"]>=85]
        ),

        "average_confidence":
        round(
            sum(x["confidence"] for x in top)/len(top),
            2
        ) if top else 0,

        "top_equal_highs":
        top
    }

