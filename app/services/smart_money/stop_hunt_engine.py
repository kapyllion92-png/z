def stop_hunt_engine_v11500(candles):

    if not candles:
        return {
            "tested_candles":0,
            "stop_hunts_found":0,
            "institutional_stop_hunts":0,
            "average_confidence":0,
            "top_stop_hunts":[]
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


    results=[]


    for i in range(12,len(data)-4):

        sweep=data[i]

        prev=data[i-8:i]

        eq_high=max(x["high"] for x in prev)
        eq_low=min(x["low"] for x in prev)

        swing_high=max(x["high"] for x in prev[-3:])
        swing_low=min(x["low"] for x in prev[-3:])


        future=data[i+1:i+4]

        direction=None
        score=0
        reasons=[]


        range_mid=(
            eq_high+eq_low
        )/2


        # LONG

        if sweep["low"] < eq_low and sweep["close"] > eq_low:

            direction="LONG"

            score=40

            reasons=[
                "EQUAL LOWS LIQUIDITY TAKEN",
                "STOP HUNT RECLAIM"
            ]


            if sweep["close"] <= range_mid:
                score+=10
                reasons.append(
                    "DISCOUNT ZONE"
                )


            for x in future:

                if x["close"] > swing_high:

                    score+=15

                    reasons.append(
                        "CHoCH BOS CONFIRMATION"
                    )

                    break



        # SHORT

        elif sweep["high"] > eq_high and sweep["close"] < eq_high:

            direction="SHORT"

            score=40

            reasons=[
                "EQUAL HIGHS LIQUIDITY TAKEN",
                "STOP HUNT REJECTION"
            ]


            if sweep["close"] >= range_mid:

                score+=10

                reasons.append(
                    "PREMIUM ZONE"
                )


            for x in future:

                if x["close"] < swing_low:

                    score+=15

                    reasons.append(
                        "CHoCH BOS CONFIRMATION"
                    )

                    break



        if not direction:
            continue


        if future:

            confirm=future[0]

            candle_range=(
                confirm["high"]-
                confirm["low"]
            )

            if candle_range:

                body=abs(
                    confirm["close"]-
                    confirm["open"]
                )


                if body/candle_range>=0.3:

                    score+=15

                    reasons.append(
                        "DISPLACEMENT CONFIRMED"
                    )


            if confirm["volume"]>=sweep["volume"]:

                score+=10

                reasons.append(
                    "VOLUME CONFIRMATION"
                )



        if score>=85:

            results.append({

                "event":
                f"{direction} STOP HUNT INSTITUTIONAL v11500",

                "type":
                "SMART MONEY STOP HUNT",

                "direction":
                direction,

                "zone":
                [
                    round(sweep["low"],2),
                    round(sweep["high"],2)
                ],

                "score":
                min(score,100),

                "confidence":
                min(score,100),

                "quality":
                "A+ INSTITUTIONAL PREMIUM"
                if score>=90
                else
                "A INSTITUTIONAL",

                "fresh":
                True,

                "status":
                "ACTIVE",

                "reasons":
                reasons

            })



    # объединение близких зон

    unique=[]


    for r in sorted(
        results,
        key=lambda x:x["confidence"],
        reverse=True
    ):

        duplicate=False


        for u in unique:

            if (
                r["direction"]==u["direction"]
                and
                abs(
                    r["zone"][0]-
                    u["zone"][0]
                )<0.15
            ):

                duplicate=True
                break


        if not duplicate:

            unique.append(r)



    avg=round(
        sum(x["confidence"] for x in unique)
        /
        len(unique),
        2
    ) if unique else 0



    return {

        "tested_candles":
        len(data),

        "stop_hunts_found":
        len(unique),

        "institutional_stop_hunts":
        len(
            [
                x for x in unique
                if x["confidence"]>=85
            ]
        ),

        "average_confidence":
        avg,

        "top_stop_hunts":
        unique[:10]
    }
