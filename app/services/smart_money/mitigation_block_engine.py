def mitigation_block_engine_v10800(candles):

    if not candles:
        return {
            "tested_candles":0,
            "mitigation_blocks_found":0,
            "institutional_mitigations":0,
            "average_confidence":0,
            "top_mitigations":[]
        }


    data=[]

    for c in candles:
        try:
            if isinstance(c,dict):
                data.append({
                    "open":float(c["open"]),
                    "high":float(c["high"]),
                    "low":float(c["low"]),
                    "close":float(c["close"]),
                    "volume":float(c.get("volume",0))
                })
            else:
                data.append({
                    "open":float(c[1]),
                    "high":float(c[2]),
                    "low":float(c[3]),
                    "close":float(c[4]),
                    "volume":float(c[5]) if len(c)>5 else 0
                })
        except:
            continue


    blocks=[]


    for i in range(8,len(data)-2):

        candidates=data[i-6:i-2]


        for ob in candidates:

            ob_index=data.index(ob)

            impulse=None


            for x in range(ob_index+1,min(ob_index+4,len(data))):

                c=data[x]


                if (
                    ob["close"] < ob["open"]
                    and
                    c["close"] > ob["high"]
                ):
                    impulse=c
                    direction="LONG"
                    break


                if (
                    ob["close"] > ob["open"]
                    and
                    c["close"] < ob["low"]
                ):
                    impulse=c
                    direction="SHORT"
                    break


            if not impulse:
                continue


            retest=data[i]


            zone=[
                ob["low"],
                ob["high"]
            ]


            if direction=="LONG":

                if not (
                    retest["low"] <= zone[1]
                    and
                    retest["close"] >= zone[0]
                ):
                    continue


                reasons=[
                    "ORDER BLOCK SOURCE",
                    "MITIGATION RETEST",
                    "BULLISH RECLAIM"
                ]


            else:

                if not (
                    retest["high"] >= zone[0]
                    and
                    retest["close"] <= zone[1]
                ):
                    continue


                reasons=[
                    "ORDER BLOCK SOURCE",
                    "MITIGATION RETEST",
                    "BEARISH REJECTION"
                ]


            score=80


            rng=impulse["high"]-impulse["low"]

            if rng:

                body=abs(
                    impulse["close"]-
                    impulse["open"]
                )

                if body/rng>=0.25:
                    score+=5
                    reasons.append(
                        "DISPLACEMENT CONFIRMED"
                    )


            if impulse["volume"]>=ob["volume"]:
                score+=5
                reasons.append(
                    "VOLUME CONFIRMATION"
                )


            blocks.append({

                "event":
                f"{direction} MITIGATION BLOCK INSTITUTIONAL v10800",

                "type":
                "SMART MONEY MITIGATION BLOCK",

                "direction":
                direction,

                "zone":[
                    round(zone[0],2),
                    round(zone[1],2)
                ],

                "score":
                min(score,100),

                "confidence":
                min(score,100),

                "quality":
                "A+ INSTITUTIONAL PREMIUM"
                if score>=95
                else
                "A INSTITUTIONAL",

                "fresh":True,

                "status":"ACTIVE",

                "reasons":reasons
            })


    blocks=sorted(
        blocks,
        key=lambda x:x["confidence"],
        reverse=True
    )


    unique=[]

    for b in blocks:

        if not any(
            b["direction"]==u["direction"]
            and abs(b["zone"][0]-u["zone"][0])<0.05
            for u in unique
        ):
            unique.append(b)


    unique=unique[:10]


    avg=round(
        sum(x["confidence"] for x in unique)/len(unique),
        2
    ) if unique else 0


    return {
        "tested_candles":len(data),
        "mitigation_blocks_found":len(unique),
        "institutional_mitigations":len(
            [
                x for x in unique
                if x["confidence"]>=85
            ]
        ),
        "average_confidence":avg,
        "top_mitigations":unique
    }
