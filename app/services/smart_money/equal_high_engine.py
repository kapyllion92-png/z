def equal_high_engine_v100(candles):

    highs=[]

    for c in candles:

        if isinstance(c,dict):
            highs.append(float(c["high"]))
        else:
            highs.append(float(c[2]))


    pools=[]


    tolerance=0.003


    for i in range(len(highs)-5):

        cluster=[]

        base=highs[i]


        for j in range(i+1,len(highs)):

            diff=abs(highs[j]-base)/base


            if diff<=tolerance:

                cluster.append(highs[j])


        if len(cluster)>=2:

            level=sum(cluster+[base])/(len(cluster)+1)


            strength=len(cluster)+1


            score=40


            reasons=[
                "EQUAL HIGHS LIQUIDITY POOL"
            ]


            if strength>=3:
                score+=20
                reasons.append(
                    "STRONG LIQUIDITY CLUSTER"
                )


            if strength>=5:
                score+=15
                reasons.append(
                    "INSTITUTIONAL LIQUIDITY"
                )


            pools.append({

                "event":
                "BUY SIDE EQUAL HIGHS LIQUIDITY",


                "type":
                "BUY SIDE LIQUIDITY POOL",


                "level":
                round(level,4),


                "pool_strength":
                strength,


                "score":
                min(score,100),


                "confidence":
                min(score,100),


                "quality":
                "INSTITUTIONAL PREMIUM"
                if score>=75
                else "HIGH"
                if score>=55
                else "NORMAL",


                "status":
                "ACTIVE",


                "reasons":
                reasons

            })


    unique=[]

    seen=set()


    for p in pools:

        key=round(p["level"],2)

        if key not in seen:

            seen.add(key)
            unique.append(p)



    unique=sorted(
        unique,
        key=lambda x:x["score"],
        reverse=True
    )


    return {

        "tested_candles":
        len(candles),


        "equal_highs_found":
        len(unique),


        "institutional_pools":
        len(
            [
                x for x in unique
                if x["score"]>=75
            ]
        ),


        "average_confidence":
        round(
            sum(
                x["confidence"]
                for x in unique
            )
            /
            len(unique),
            2
        )
        if unique else 0,


        "top_equal_highs":
        unique[:10]

    }

