def equal_levels_engine_v12000(candles):

    if not candles:
        return {
            "tested_candles":0,
            "equal_highs_found":0,
            "equal_lows_found":0,
            "institutional_levels":0,
            "average_strength":0,
            "top_levels":[]
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



    levels=[]


    tolerance=0.0025


    for i in range(5,len(data)-5):

        current=data[i]


        highs=[]
        lows=[]


        for x in range(i-5,i):

            highs.append(data[x]["high"])
            lows.append(data[x]["low"])



        # Equal Highs

        high_matches=[
            h for h in highs
            if abs(h-current["high"])
            /
            current["high"]
            <= tolerance
        ]


        if len(high_matches)>=2:


            touches=len(high_matches)+1

            strength=50

            reasons=[
                "EQUAL HIGHS LIQUIDITY POOL"
            ]


            if touches>=3:

                strength+=20

                reasons.append(
                    "MULTIPLE TOUCHES"
                )


            if current["volume"]>0:

                strength+=10

                reasons.append(
                    "VOLUME CONTEXT"
                )


            levels.append({

                "event":
                "EQUAL HIGHS INSTITUTIONAL v12000",

                "type":
                "BUY SIDE LIQUIDITY POOL",

                "direction":
                "SHORT AFTER SWEEP",

                "zone":[
                    round(current["high"]*0.998,2),
                    round(current["high"]*1.002,2)
                ],

                "touches":
                touches,

                "strength":
                min(strength,100),

                "confidence":
                min(strength,100),

                "quality":
                "A INSTITUTIONAL"
                if strength>=80
                else
                "B QUALITY",

                "status":
                "ACTIVE",

                "reasons":
                reasons
            })




        # Equal Lows


        low_matches=[

            l for l in lows

            if abs(l-current["low"])
            /
            current["low"]
            <= tolerance

        ]


        if len(low_matches)>=2:


            touches=len(low_matches)+1


            strength=50


            reasons=[
                "EQUAL LOWS LIQUIDITY POOL"
            ]


            if touches>=3:

                strength+=20

                reasons.append(
                    "MULTIPLE TOUCHES"
                )


            if current["volume"]>0:

                strength+=10

                reasons.append(
                    "VOLUME CONTEXT"
                )



            levels.append({

                "event":
                "EQUAL LOWS INSTITUTIONAL v12000",

                "type":
                "SELL SIDE LIQUIDITY POOL",

                "direction":
                "LONG AFTER SWEEP",

                "zone":[
                    round(current["low"]*0.998,2),
                    round(current["low"]*1.002,2)
                ],

                "touches":
                touches,

                "strength":
                min(strength,100),

                "confidence":
                min(strength,100),

                "quality":
                "A INSTITUTIONAL"
                if strength>=80
                else
                "B QUALITY",

                "status":
                "ACTIVE",

                "reasons":
                reasons
            })



    levels=sorted(
        levels,
        key=lambda x:x["confidence"],
        reverse=True
    )


    unique=[]


    for l in levels:

        duplicate=False


        for u in unique:

            if (

                l["type"]==u["type"]

                and

                abs(
                    l["zone"][0]-
                    u["zone"][0]
                )<0.05

            ):

                duplicate=True
                break


        if not duplicate:

            unique.append(l)



    avg=round(

        sum(
            x["confidence"]
            for x in unique
        )
        /
        len(unique),

        2

    ) if unique else 0



    return {

        "tested_candles":
        len(data),

        "equal_highs_found":
        len([
            x for x in unique
            if "HIGHS" in x["event"]
        ]),

        "equal_lows_found":
        len([
            x for x in unique
            if "LOWS" in x["event"]
        ]),

        "institutional_levels":
        len([
            x for x in unique
            if x["confidence"]>=70
        ]),

        "average_strength":
        avg,

        "top_levels":
        unique[:10]

    }
