def _num(v):
    try:
        return float(v)
    except:
        return 0.0


def _get(c, key):

    if isinstance(c, dict):
        return _num(c.get(key, 0))

    pos = {
        "open": 1,
        "high": 2,
        "low": 3,
        "close": 4,
        "volume": 5
    }

    try:
        return _num(c[pos[key]])
    except:
        return 0.0



def liquidity_sweep_engine_v2700(candles):

    tested = len(candles)

    highs = []
    lows = []


    for i in range(3, len(candles)-3):

        h = _get(candles[i],"high")
        l = _get(candles[i],"low")


        if h >= max(_get(candles[x],"high") for x in range(i-3,i)) and h >= max(_get(candles[x],"high") for x in range(i+1,i+4)):
            highs.append({"level":h,"index":i})


        if l <= min(_get(candles[x],"low") for x in range(i-3,i)) and l <= min(_get(candles[x],"low") for x in range(i+1,i+4)):
            lows.append({"level":l,"index":i})


    def cluster(data):

        result=[]

        for x in data:

            if not any(
                abs(x["level"]-y["level"])/max(y["level"],0.001)<0.0015
                for y in result
            ):
                result.append(x)

        return result



    high_clusters = cluster(highs)
    low_clusters = cluster(lows)


    sweeps=[]
    used=set()


    for i,c in enumerate(candles):

        if i==0:
            continue


        high=_get(c,"high")
        low=_get(c,"low")
        close=_get(c,"close")
        open_=_get(c,"open")
        volume=_get(c,"volume")


        rng=max(high-low,0.0001)
        body=max(abs(close-open_),0.0001)

        wick_strength=body/rng < 0.45

        displacement=body/rng > 0.55


        prev_close=_get(candles[i-1],"close")


        choch=abs(close-prev_close)/max(prev_close,0.001)>0.002

        bos=choch


        for side,clusters in [
            ("HIGH",high_clusters),
            ("LOW",low_clusters)
        ]:

            for idx,pool in enumerate(clusters):

                key=(side,idx)

                if key in used:
                    continue


                level=pool["level"]

                age=i-pool["index"]

                if age<5:
                    continue


                score=0
                reasons=[]


                if side=="HIGH":

                    if high>=level and close<level:

                        score+=20
                        reasons.append("EQUAL HIGHS LIQUIDITY TAKEN")

                        direction="BEARISH"

                    else:
                        continue


                else:

                    if low<=level and close>level:

                        score+=20
                        reasons.append("EQUAL LOWS LIQUIDITY TAKEN")

                        direction="BULLISH"

                    else:
                        continue



                score+=15
                reasons.append("STOP HUNT CONFIRMED")


                if wick_strength:

                    score+=15
                    reasons.append("WICK REJECTION")


                if age>50:

                    score+=10
                    reasons.append("AGE CONFIRMATION")


                if volume>0:

                    score+=10
                    reasons.append("VOLUME CONFIRMATION")



                if choch:

                    score+=15
                    reasons.append("CHoCH CONFIRMATION")


                if bos:

                    score+=10
                    reasons.append("BOS CONFIRMATION")



                if displacement:

                    score+=10
                    reasons.append("DISPLACEMENT CANDLE")



                # proxy confirmations
                if len(candles)-i < 20:

                    score+=10
                    reasons.append("FRESH SWEEP")



                score=min(score,100)



                if score>=95:

                    quality="A+ INSTITUTIONAL PREMIUM"

                elif score>=85:

                    quality="A INSTITUTIONAL"

                elif score>=75:

                    quality="B QUALITY"

                else:

                    continue



                sweeps.append({

                    "event":
                    f"{'BUY SIDE' if side=='HIGH' else 'SELL SIDE'} LIQUIDITY SWEEP INSTITUTIONAL v2700",

                    "type":
                    "SMART MONEY LIQUIDITY SWEEP",

                    "level":
                    round(level,4),

                    "direction":
                    direction,

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


                used.add(key)



    return {

        "tested_candles":tested,

        "equal_high_clusters":len(high_clusters),

        "equal_low_clusters":len(low_clusters),

        "sweeps_found":len(sweeps),

        "institutional_sweeps":
        len([x for x in sweeps if x["quality"].startswith("A")]),

        "average_confidence":
        round(
            sum(x["confidence"] for x in sweeps)/len(sweeps),2
        ) if sweeps else 0,

        "top_sweeps":
        sweeps[:10]

    }

