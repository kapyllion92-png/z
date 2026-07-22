def breaker_block_engine_v7000(candles):

    if not candles:
        return {
            "tested_candles":0,
            "breaker_blocks_found":0,
            "institutional_breakers":0,
            "average_confidence":0,
            "top_breakers":[]
        }


    def val(c,k):
        if isinstance(c,dict):
            return float(c[k])

        mp={
            "open":1,
            "high":2,
            "low":3,
            "close":4,
            "volume":5
        }
        return float(c[mp[k]])


    volume_avg=sum(
        val(c,"volume")
        for c in candles
    )/len(candles)


    ranges=[
        val(c,"high")-val(c,"low")
        for c in candles
    ]

    atr=sum(ranges)/len(ranges)


    breakers=[]


    for i in range(10,len(candles)-2):

        ob=candles[i-3]
        sweep=candles[i-2]
        confirm=candles[i-1]
        current=candles[i]


        oo=val(ob,"open")
        oc=val(ob,"close")
        oh=val(ob,"high")
        ol=val(ob,"low")


        sh=val(sweep,"high")
        sl=val(sweep,"low")


        co=val(confirm,"open")
        cc=val(confirm,"close")
        ch=val(confirm,"high")
        cl=val(confirm,"low")
        cv=val(confirm,"volume")


        current_close=val(current,"close")


        body=abs(cc-co)
        candle_range=ch-cl

        if candle_range==0:
            continue


        displacement = body/candle_range >=0.45

        volume_confirmation=cv >= volume_avg


        liquidity_taken_low = sl < min(
            val(x,"low")
            for x in candles[i-8:i-2]
        )

        liquidity_taken_high = sh > max(
            val(x,"high")
            for x in candles[i-8:i-2]
        )


        bos_up=current_close > max(
            val(x,"high")
            for x in candles[i-8:i-1]
        )

        bos_down=current_close < min(
            val(x,"low")
            for x in candles[i-8:i-1]
        )


        zone=[
            round(min(ol,oh),2),
            round(max(ol,oh),2)
        ]


        score=0
        reasons=[]


        # BULLISH BREAKER
        if oc < oo and cc > oh:

            score+=30
            reasons.append(
                "BEARISH ORDER BLOCK INVALIDATED"
            )

            score+=15
            reasons.append(
                "BULLISH RECLAIM"
            )


            if displacement:
                score+=15
                reasons.append(
                    "DISPLACEMENT CONFIRMED"
                )


            if volume_confirmation:
                score+=10
                reasons.append(
                    "VOLUME CONFIRMATION"
                )


            if liquidity_taken_low:
                score+=15
                reasons.append(
                    "LIQUIDITY TAKEN"
                )


            if bos_up:
                score+=15
                reasons.append(
                    "CHoCH BOS CONFIRMATION"
                )


            if score>=80:

                breakers.append({

                    "event":
                    "BULLISH BREAKER BLOCK INSTITUTIONAL v7000",

                    "type":
                    "SMART MONEY BREAKER BLOCK",

                    "direction":"LONG",

                    "zone":zone,

                    "score":score,

                    "confidence":score,

                    "quality":
                    "A+ INSTITUTIONAL PREMIUM"
                    if score>=95 else
                    "A INSTITUTIONAL"
                    if score>=85 else
                    "B QUALITY",

                    "fresh":True,

                    "status":"ACTIVE",

                    "reasons":reasons
                })



        # BEARISH BREAKER
        if oc > oo and cc < ol:

            score+=30

            reasons.append(
                "BULLISH ORDER BLOCK INVALIDATED"
            )

            score+=15

            reasons.append(
                "BEARISH REJECTION"
            )


            if displacement:
                score+=15
                reasons.append(
                    "DISPLACEMENT CONFIRMED"
                )


            if volume_confirmation:
                score+=10
                reasons.append(
                    "VOLUME CONFIRMATION"
                )


            if liquidity_taken_high:
                score+=15
                reasons.append(
                    "LIQUIDITY TAKEN"
                )


            if bos_down:
                score+=15
                reasons.append(
                    "CHoCH BOS CONFIRMATION"
                )


            if score>=80:

                breakers.append({

                    "event":
                    "BEARISH BREAKER BLOCK INSTITUTIONAL v7000",

                    "type":
                    "SMART MONEY BREAKER BLOCK",

                    "direction":"SHORT",

                    "zone":zone,

                    "score":score,

                    "confidence":score,

                    "quality":
                    "A+ INSTITUTIONAL PREMIUM"
                    if score>=95 else
                    "A INSTITUTIONAL"
                    if score>=85 else
                    "B QUALITY",

                    "fresh":True,

                    "status":"ACTIVE",

                    "reasons":reasons
                })


    # дедупликация зон

    final=[]

    for b in sorted(
        breakers,
        key=lambda x:x["score"],
        reverse=True
    ):

        mid=sum(b["zone"])/2

        duplicate=False

        for f in final:

            mid2=sum(f["zone"])/2

            if abs(mid-mid2)/mid <0.003:
                duplicate=True
                break

        if not duplicate:
            final.append(b)



    return {

        "tested_candles":len(candles),

        "breaker_blocks_found":len(final),

        "institutional_breakers":len(
            [
                x for x in final
                if x["score"]>=85
            ]
        ),

        "average_confidence":
        round(
            sum(x["confidence"] for x in final)
            /
            len(final),
            2
        )
        if final else 0,

        "top_breakers":final[:10]
    }
