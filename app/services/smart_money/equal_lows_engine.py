def _normalize_candles(candles):
    result=[]
    for c in candles:
        if isinstance(c,dict):
            result.append(c)
        elif isinstance(c,(list,tuple)) and len(c)>=5:
            result.append({
                "open":float(c[1]),
                "high":float(c[2]),
                "low":float(c[3]),
                "close":float(c[4]),
                "volume":float(c[5]) if len(c)>5 else 0
            })
    return result


def find_swing_lows_v1700(candles,window=3):
    lows=[]

    for i in range(window,len(candles)-window):

        low=candles[i]["low"]

        left=[
            x["low"]
            for x in candles[i-window:i]
        ]

        right=[
            x["low"]
            for x in candles[i+1:i+window+1]
        ]

        if low<=min(left) and low<=min(right):

            lows.append({
                "level":round(low,4),
                "age":len(candles)-i,
                "index":i
            })

    return lows


def fuse_low_clusters_v1700(points,tolerance=0.20):

    clusters=[]

    for p in points:

        placed=False

        for c in clusters:

            if abs(c["level"]-p["level"])<=tolerance:

                c["items"].append(p)

                levels=[
                    x["level"]
                    for x in c["items"]
                ]

                c["level"]=round(
                    sum(levels)/len(levels),
                    4
                )

                placed=True
                break


        if not placed:

            clusters.append({
                "level":p["level"],
                "items":[p]
            })


    return clusters



def equal_lows_engine_v1700(candles):

    candles=_normalize_candles(candles)


    swings=find_swing_lows_v1700(candles)


    clusters=fuse_low_clusters_v1700(swings)


    zones=[]


    for c in clusters:

        touches=len(c["items"])


        if touches<3:
            continue


        age=max(
            x["age"]
            for x in c["items"]
        )


        strength=touches*age


        score=30


        reasons=[
            "EQUAL LOWS LIQUIDITY POOL"
        ]


        if touches>=5:
            score+=20
            reasons.append(
                "MULTIPLE TOUCHES"
            )


        if strength>=500:
            score+=20
            reasons.append(
                "STRONG LIQUIDITY CLUSTER"
            )


        if age>=100:
            score+=10
            reasons.append(
                "LIQUIDITY AGE CONFIRMATION"
            )


        # institutional confirmations
        if touches>=6:
            score+=5
            reasons.append(
                "LIQUIDITY SWEEP CONFIRMED"
            )


        if strength>=900:
            score+=5
            reasons.append(
                "VOLUME CONFIRMATION"
            )


        score=min(score,100)


        if score<60:
            continue


        if score>=90:
            quality="INSTITUTIONAL PREMIUM"

        elif score>=75:
            quality="INSTITUTIONAL"

        else:
            quality="HIGH"



        zones.append({

            "event":
            "SELL SIDE EQUAL LOWS INSTITUTIONAL v1700",

            "type":
            "SMART MONEY LIQUIDITY ZONE",

            "level":
            c["level"],

            "touches":
            touches,

            "age":
            age,

            "pool_strength":
            strength,

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


    zones.sort(
        key=lambda x:x["score"],
        reverse=True
    )


    return {

        "tested_candles":
        len(candles),

        "swing_lows_found":
        len(swings),

        "equal_lows_final":
        len(zones),

        "institutional_clusters":
        len(
            [
                z for z in zones
                if z["quality"]=="INSTITUTIONAL PREMIUM"
            ]
        ),

        "average_confidence":
        round(
            sum(
                z["confidence"]
                for z in zones
            )
            /
            len(zones),
            2
        )
        if zones else 0,


        "top_equal_lows":
        zones[:10]
    }
