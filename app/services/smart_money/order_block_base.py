def order_block_engine_v14000(candles):

    if not candles:
        return {
            "tested_candles":0,
            "order_blocks_found":0,
            "institutional_order_blocks":0,
            "average_confidence":0,
            "top_order_blocks":[]
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


    for i in range(5,len(data)-5):

        ob=data[i-2]
        impulse=data[i-1]
        confirm=data[i+1]


        direction=None
        reasons=[]


        score=0



        if (
            ob["close"] < ob["open"]
            and
            impulse["close"] > ob["high"]
        ):

            direction="LONG"

            score=40

            reasons.append(
                "ORDER BLOCK SOURCE"
            )


        elif (
            ob["close"] > ob["open"]
            and
            impulse["close"] < ob["low"]
        ):

            direction="SHORT"

            score=40

            reasons.append(
                "ORDER BLOCK SOURCE"
            )


        if not direction:
            continue



        rng=max(
            impulse["high"]-impulse["low"],
            0.00001
        )


        body=abs(
            impulse["close"]-
            impulse["open"]
        )


        if body/rng >= 0.2:

            score+=20

            reasons.append(
                "STRONG DISPLACEMENT"
            )



        if direction=="LONG":

            if confirm["close"]>impulse["high"]:

                score+=15

                reasons.append(
                    "BOS CHoCH CONFIRMATION"
                )


            if confirm["low"]<=ob["high"]:

                score+=10

                reasons.append(
                    "MITIGATION"
                )


        else:

            if confirm["close"]<impulse["low"]:

                score+=15

                reasons.append(
                    "BOS CHoCH CONFIRMATION"
                )


            if confirm["high"]>=ob["low"]:

                score+=10

                reasons.append(
                    "MITIGATION"
                )



        if impulse["volume"]>=ob["volume"]:

            score+=10

            reasons.append(
                "VOLUME CONFIRMATION"
            )


        score+=5

        reasons.append(
            "FRESH INSTITUTIONAL BLOCK"
        )


        blocks.append({

            "direction":direction,

            "zone":[
                ob["low"],
                ob["high"]
            ],

            "score":
            min(score,100),

            "confidence":
            min(score,100),

            "reasons":
            reasons

        })



    clusters=[]


    for b in blocks:

        found=False


        for c in clusters:

            if (
                b["direction"]==c["direction"]
                and
                b["zone"][0]<=c["high"]+0.25
                and
                b["zone"][1]>=c["low"]-0.25
            ):

                c["low"]=min(
                    c["low"],
                    b["zone"][0]
                )

                c["high"]=max(
                    c["high"],
                    b["zone"][1]
                )

                c["score"]+=b["score"]

                c["sources"]+=1

                found=True

                break


        if not found:

            clusters.append({

                "direction":b["direction"],

                "low":b["zone"][0],

                "high":b["zone"][1],

                "score":b["score"],

                "sources":1,

                "reasons":b["reasons"]

            })



    result=[]


    for c in clusters:

        confidence=min(
            100,
            int(c["score"]/c["sources"]+20)
        )


        if confidence>=80:

            result.append({

                "event":
                f"{c['direction']} ORDER BLOCK CLUSTER INSTITUTIONAL v14000",

                "type":
                "SMART MONEY ORDER BLOCK CLUSTER",

                "direction":
                c["direction"],

                "zone":[
                    round(c["low"],2),
                    round(c["high"],2)
                ],

                "score":
                confidence,

                "confidence":
                confidence,

                "quality":
                "A+ INSTITUTIONAL PREMIUM",

                "source_blocks":
                c["sources"],

                "status":
                "ACTIVE",

                "reasons":
                c["reasons"]

            })


    return {

        "tested_candles":
        len(data),

        "order_blocks_found":
        len(result),

        "institutional_order_blocks":
        len(result),

        "average_confidence":
        round(
            sum(x["confidence"] for x in result)
            /
            len(result),
            2
        ) if result else 0,

        "top_order_blocks":
        result[:10]

    }
