
def analyze_liquidity(candles):

    result = {
        "liquidity_sweep": False,
        "liquidity_grab": False,
        "stop_hunt": False,
        "return_after_sweep": False,
        "volume_confirmation": False,
        "atr_confirmation": False,
        "structure_confirmation": False,
        "direction": None,
        "score": 0,
        "reasons": [],
        "quality": "LOW"
    }

    if not candles:
        return result


    highs = [float(c[2]) if isinstance(c,list) else float(c["high"]) for c in candles]
    lows = [float(c[3]) if isinstance(c,list) else float(c["low"]) for c in candles]
    closes = [float(c[4]) if isinstance(c,list) else float(c["close"]) for c in candles]
    opens = [float(c[1]) if isinstance(c,list) else float(c["open"]) for c in candles]
    volumes = [float(c[5]) if isinstance(c,list) else float(c.get("volume",0)) for c in candles]


    last_high = highs[-1]
    last_low = lows[-1]
    last_close = closes[-1]
    last_open = opens[-1]


    # ==========================
    # BASIC LIQUIDITY SWEEP
    # ==========================

    if len(candles) >= 5:

        previous_high = max(highs[-5:-1])
        previous_low = min(lows[-5:-1])


        # SELL SIDE SWEEP
        if last_low < previous_low and last_close > previous_low:

            result["liquidity_sweep"] = True
            result["liquidity_grab"] = True
            result["direction"] = "LONG"
            result["score"] += 20
            result["reasons"].append(
                "SELL SIDE LIQUIDITY SWEEP"
            )


        # BUY SIDE SWEEP
        elif last_high > previous_high and last_close < previous_high:

            result["liquidity_sweep"] = True
            result["liquidity_grab"] = True
            result["direction"] = "SHORT"
            result["score"] += 20
            result["reasons"].append(
                "BUY SIDE LIQUIDITY SWEEP"
            )


    # ==========================
    # VOLUME CONFIRMATION
    # ==========================

    avg_volume = sum(volumes[-20:]) / max(len(volumes[-20:]),1)

    if volumes[-1] > avg_volume * 1.3:

        result["volume_confirmation"] = True
        result["score"] += 10
        result["reasons"].append(
            "VOLUME CONFIRMATION"
        )


    # ==========================
    # WICK REJECTION FILTER
    # ==========================

    body = abs(last_close-last_open)

    upper_wick = last_high - max(last_open,last_close)
    lower_wick = min(last_open,last_close)-last_low


    if result["direction"] == "LONG":

        if lower_wick > body * 1.5:

            result["score"] += 15
            result["reasons"].append(
                "STRONG LOWER WICK REJECTION"
            )


    if result["direction"] == "SHORT":

        if upper_wick > body * 1.5:

            result["score"] += 15
            result["reasons"].append(
                "STRONG UPPER WICK REJECTION"
            )


    # ==========================
    # ATR EXPANSION
    # ==========================

    ranges = [
        highs[i]-lows[i]
        for i in range(max(0,len(highs)-20),len(highs))
    ]

    if ranges:

        atr = sum(ranges)/len(ranges)

        if ranges[-1] > atr * 1.2:

            result["atr_confirmation"] = True
            result["score"] += 10
            result["reasons"].append(
                "ATR EXPANSION"
            )


    # ==========================
    # STRUCTURE CONFIRMATION BOS
    # ==========================

    if len(highs) >= 10:

        previous_high = max(highs[-10:-1])
        previous_low = min(lows[-10:-1])


        if last_close > previous_high:

            result["structure_confirmation"] = True
            result["score"] += 10
            result["reasons"].append(
                "BULLISH BOS"
            )


        elif last_close < previous_low:

            result["structure_confirmation"] = True
            result["score"] += 10
            result["reasons"].append(
                "BEARISH BOS"
            )


    # ==========================
    # QUALITY
    # ==========================

    if result["score"] >= 70:
        result["quality"] = "PREMIUM"

    elif result["score"] >= 50:
        result["quality"] = "GOOD"

    elif result["score"] >= 30:
        result["quality"] = "MEDIUM"


    return result


def liquidity_sweep_premium_filter(result, candles):

    score=result.get("score",0)

    reasons=result.setdefault(
        "reasons",
        []
    )


    # ==========================
    # WICK CONFIRMATION
    # ==========================

    last=candles[-1]


    if isinstance(last,list):

        high=float(last[2])
        low=float(last[3])
        close=float(last[4])
        open_price=float(last[1])

    else:

        high=float(last["high"])
        low=float(last["low"])
        close=float(last["close"])
        open_price=float(last["open"])


    body=abs(close-open_price)

    upper_wick=high-max(close,open_price)

    lower_wick=min(close,open_price)-low


    if upper_wick > body*1.5:

        result["wick_confirmation"]=True

        score+=10

        reasons.append(
            "UPPER WICK REJECTION"
        )


    if lower_wick > body*1.5:

        result["wick_confirmation"]=True

        score+=10

        reasons.append(
            "LOWER WICK REJECTION"
        )


    # ==========================
    # DISPLACEMENT
    # ==========================

    if len(candles)>=5:

        prev=candles[-5]


        prev_close=float(prev[4]) if isinstance(prev,list) else float(prev["close"])


        move=abs(close-prev_close)


        if move > body*2:

            result["displacement_confirmation"]=True

            score+=10

            reasons.append(
                "PRICE DISPLACEMENT"
            )


    # ==========================
    # SWEEP PROBABILITY
    # ==========================

    probability=0


    if result.get("liquidity_sweep"):

        probability+=40


    if result.get("volume_confirmation"):

        probability+=20


    if result.get("wick_confirmation"):

        probability+=20


    if result.get("displacement_confirmation"):

        probability+=20


    result["sweep_probability"]=min(
        probability,
        100
    )


    score=max(
        0,
        min(score,100)
    )


    result["score"]=score

    result["ai_probability"]=score


    if score>=90:

        result["quality"]="PREMIUM"

    elif score>=75:

        result["quality"]="HIGH"

    elif score>=50:

        result["quality"]="MEDIUM"

    else:

        result["quality"]="LOW"


    return result



def liquidity_sweep_confirmation_engine(result, candles):

    score=result.get("score",0)

    reasons=result.setdefault(
        "reasons",
        []
    )


    highs=[]
    lows=[]
    closes=[]
    opens=[]


    for c in candles:

        if isinstance(c,list):

            opens.append(float(c[1]))
            highs.append(float(c[2]))
            lows.append(float(c[3]))
            closes.append(float(c[4]))

        else:

            opens.append(float(c["open"]))
            highs.append(float(c["high"]))
            lows.append(float(c["low"]))
            closes.append(float(c["close"]))


    # ==========================
    # RETURN AFTER SWEEP
    # ==========================

    if result.get("liquidity_sweep") and len(candles)>=5:

        last_close=closes[-1]

        recent_high=max(highs[-5:])
        recent_low=min(lows[-5:])


        if last_close < recent_high and last_close > recent_low:

            result["return_after_sweep"]=True

            score+=15

            reasons.append(
                "RETURN INSIDE LIQUIDITY RANGE"
            )


    # ==========================
    # WICK CONFIRMATION PREMIUM
    # ==========================

    high=highs[-1]
    low=lows[-1]
    close=closes[-1]
    open_price=opens[-1]


    body=abs(close-open_price)

    upper_wick=high-max(close,open_price)

    lower_wick=min(close,open_price)-low


    if lower_wick > body*2:

        result["wick_confirmation"]=True

        score+=10

        reasons.append(
            "SELL SIDE WICK REJECTION"
        )


    if upper_wick > body*2:

        result["wick_confirmation"]=True

        score+=10

        reasons.append(
            "BUY SIDE WICK REJECTION"
        )


    # ==========================
    # DISPLACEMENT
    # ==========================

    if len(closes)>=6:

        impulse=abs(
            closes[-1]-closes[-6]
        )

        avg_move=sum(
            abs(closes[i]-closes[i-1])
            for i in range(
                len(closes)-10,
                len(closes)
            )
        )/10


        if impulse > avg_move*3:

            result["displacement_confirmation"]=True

            score+=15

            reasons.append(
                "INSTITUTIONAL DISPLACEMENT"
            )


    # ==========================
    # BOS CONFIRMATION
    # ==========================

    if len(closes)>=20:

        previous_high=max(
            highs[-20:-1]
        )

        previous_low=min(
            lows[-20:-1]
        )


        if closes[-1] > previous_high:

            result["structure_confirmation"]=True

            result["direction"]="LONG"

            score+=15

            reasons.append(
                "BULLISH BOS"
            )


        elif closes[-1] < previous_low:

            result["structure_confirmation"]=True

            result["direction"]="SHORT"

            score+=15

            reasons.append(
                "BEARISH BOS"
            )


    # ==========================
    # FINAL AI SCORE
    # ==========================

    probability=0


    if result.get("liquidity_sweep"):
        probability+=30

    if result.get("return_after_sweep"):
        probability+=20

    if result.get("wick_confirmation"):
        probability+=15

    if result.get("displacement_confirmation"):
        probability+=20

    if result.get("structure_confirmation"):
        probability+=15


    result["sweep_probability"]=min(
        probability,
        100
    )


    score=max(
        0,
        min(score,100)
    )


    result["score"]=score

    result["ai_probability"]=score


    if score>=90:

        result["quality"]="PREMIUM"

    elif score>=75:

        result["quality"]="HIGH"

    elif score>=50:

        result["quality"]="MEDIUM"

    else:

        result["quality"]="LOW"


    return result




def liquidity_sweep_institutional_confirmation(result, candles):

    score=result.get("score",0)

    reasons=result.setdefault(
        "reasons",
        []
    )


    volumes=[]

    highs=[]
    lows=[]
    closes=[]
    opens=[]


    for c in candles:

        if isinstance(c,list):

            opens.append(float(c[1]))
            highs.append(float(c[2]))
            lows.append(float(c[3]))
            closes.append(float(c[4]))
            volumes.append(float(c[5]))

        else:

            opens.append(float(c["open"]))
            highs.append(float(c["high"]))
            lows.append(float(c["low"]))
            closes.append(float(c["close"]))
            volumes.append(float(c.get("volume",0)))


    # ==========================
    # SMART VOLUME CONFIRMATION
    # ==========================

    if len(volumes)>=21:

        avg_volume=sum(
            volumes[-21:-1]
        )/20

        current_volume=volumes[-1]


        if current_volume > avg_volume*1.5:

            result["volume_confirmation"]=True

            score+=15

            reasons.append(
                "INSTITUTIONAL VOLUME"
            )


    # ==========================
    # WICK REJECTION
    # ==========================

    high=highs[-1]
    low=lows[-1]
    close=closes[-1]
    open_price=opens[-1]


    body=abs(
        close-open_price
    )


    if body==0:
        body=0.00001


    upper_wick=high-max(
        close,
        open_price
    )

    lower_wick=min(
        close,
        open_price
    )-low


    if lower_wick/body >=2:

        result["wick_confirmation"]=True

        score+=10

        reasons.append(
            "SELL LIQUIDITY REJECTION"
        )


    if upper_wick/body >=2:

        result["wick_confirmation"]=True

        score+=10

        reasons.append(
            "BUY LIQUIDITY REJECTION"
        )


    # ==========================
    # DISPLACEMENT
    # ==========================

    if len(closes)>=10:

        move=abs(
            closes[-1]-closes[-5]
        )


        avg_range=sum(
            abs(closes[i]-closes[i-1])
            for i in range(
                len(closes)-10,
                len(closes)
            )
        )/10


        if move > avg_range*2.5:

            result["displacement_confirmation"]=True

            score+=15

            reasons.append(
                "DISPLACEMENT MOVE"
            )


    # ==========================
    # CHOCH DETECTION
    # ==========================

    if len(closes)>=15:

        old_high=max(
            highs[-15:-5]
        )

        old_low=min(
            lows[-15:-5]
        )


        if closes[-1]>old_high:

            result["choch_confirmation"]=True

            result["direction"]="LONG"

            score+=15

            reasons.append(
                "BULLISH CHOCH"
            )


        elif closes[-1]<old_low:

            result["choch_confirmation"]=True

            result["direction"]="SHORT"

            score+=15

            reasons.append(
                "BEARISH CHOCH"
            )


    # ==========================
    # PREMIUM AI SCORE
    # ==========================

    probability=0


    if result.get("liquidity_sweep"):
        probability+=30

    if result.get("return_after_sweep"):
        probability+=15

    if result.get("wick_confirmation"):
        probability+=15

    if result.get("volume_confirmation"):
        probability+=15

    if result.get("displacement_confirmation"):
        probability+=15

    if result.get("choch_confirmation"):
        probability+=10


    result["sweep_probability"]=min(
        probability,
        100
    )


    score=max(
        0,
        min(score,100)
    )


    result["score"]=score

    result["ai_probability"]=score


    if score>=90:

        result["quality"]="PREMIUM"

    elif score>=75:

        result["quality"]="HIGH"

    elif score>=50:

        result["quality"]="MEDIUM"

    else:

        result["quality"]="LOW"


    return result





def backtest_liquidity_sweep(candles):

    signals=[]

    sweeps=0


    for i in range(30,len(candles)):

        window=candles[:i+1]


        result=analyze_liquidity(window)


        result=liquidity_sweep_confirmation_engine(
            result,
            window
        )


        result=liquidity_sweep_institutional_confirmation(
            result,
            window
        )


        result=liquidity_sweep_final_ai_validator(
            result
        )


        if result.get("liquidity_sweep"):

            sweeps+=1


        if result.get("final_quality") in [
            "HIGH",
            "PREMIUM"
        ]:


            signals.append({

                "index":i,

                "direction":
                    result.get("direction"),

                "score":
                    result.get("score"),

                "ai_probability":
                    result.get("ai_probability"),

                "quality":
                    result.get("final_quality"),

                "reasons":
                    result.get("final_reasons")

            })


    avg=0

    if signals:

        avg=sum(
            x["score"]
            for x in signals
        )/len(signals)


    return {

        "tested_candles":
            len(candles),

        "liquidity_sweeps_found":
            sweeps,

        "confirmed_signals":
            len(signals),

        "average_score":
            round(avg,2),

        "signals":
            signals[-10:]

    }



def liquidity_sweep_final_ai_validator(result):

    score=0
    probability=0
    reasons=[]


    if result.get("liquidity_sweep"):

        score+=30
        probability+=30
        reasons.append(
            "LIQUIDITY SWEEP"
        )


    if result.get("liquidity_grab"):

        score+=10
        probability+=10
        reasons.append(
            "LIQUIDITY GRAB"
        )


    if result.get("return_after_sweep"):

        score+=15
        probability+=15
        reasons.append(
            "RETURN AFTER SWEEP"
        )


    old=result.get(
        "reasons",
        []
    )

    direction=result.get(
        "direction"
    )


    if direction=="LONG":

        if any(
            ("SELL" in x or "LOWER" in x)
            for x in old
        ):

            score+=15
            probability+=15

            reasons.append(
                "SELL SIDE REJECTION"
            )


    if direction=="SHORT":

        if any(
            ("BUY" in x or "UPPER" in x)
            for x in old
        ):

            score+=15
            probability+=15

            reasons.append(
                "BUY SIDE REJECTION"
            )


    if result.get(
        "volume_confirmation"
    ):

        score+=10
        probability+=10

        reasons.append(
            "VOLUME"
        )


    if result.get(
        "displacement_confirmation"
    ):

        score+=10
        probability+=10

        reasons.append(
            "DISPLACEMENT"
        )


    if result.get(
        "choch_confirmation"
    ) or result.get(
        "structure_confirmation"
    ):

        score+=10
        probability+=10

        reasons.append(
            "STRUCTURE SHIFT"
        )


    score=min(score,100)

    probability=min(
        probability,
        100
    )


    result["score"]=score

    result["ai_probability"]=probability

    result["final_reasons"]=reasons


    if score>=90 and probability>=85:

        result["final_quality"]="PREMIUM"

    elif score>=75:

        result["final_quality"]="HIGH"

    elif score>=60:

        result["final_quality"]="MEDIUM"

    else:

        result["final_quality"]="LOW"


    return result



def liquidity_sweep_smart_money_filter(candles):

    signals=[]

    used_zones=[]


    for i in range(40,len(candles)):

        window=candles[:i+1]


        result=analyze_liquidity(
            window
        )


        result=liquidity_sweep_confirmation_engine(
            result,
            window
        )


        result=liquidity_sweep_institutional_confirmation(
            result,
            window
        )


        result=liquidity_sweep_final_ai_validator(
            result
        )


        if not result.get(
            "liquidity_sweep"
        ):

            continue


        level=None


        if isinstance(window[-1],list):

            level=float(window[-1][2])

        else:

            level=float(
                window[-1].get("high",0)
            )


        # ======================
        # ZONE COOLDOWN
        # ======================

        duplicate=False


        for z in used_zones:

            if abs(level-z)<0.3:

                duplicate=True


        if duplicate:

            continue


        used_zones.append(
            level
        )


        # ======================
        # SMART MONEY SCORE
        # ======================

        smart_score=result.get(
            "ai_probability",
            0
        )


        if result.get(
            "return_after_sweep"
        ):

            smart_score+=10


        if result.get(
            "displacement_confirmation"
        ):

            smart_score+=10


        if result.get(
            "choch_confirmation"
        ):

            smart_score+=10


        if smart_score>100:

            smart_score=100


        if smart_score>=90:

            final="PREMIUM"

        elif smart_score>=75:

            final="HIGH"

        elif smart_score>=60:

            final="MEDIUM"

        else:

            final="LOW"



        signals.append({

            "index":i,

            "direction":
                result.get(
                    "direction"
                ),

            "score":
                smart_score,

            "quality":
                final,

            "level":
                round(level,6),

            "reasons":
                result.get(
                    "final_reasons",
                    []
                )

        })


    avg=0


    if signals:

        avg=sum(
            x["score"]
            for x in signals
        )/len(signals)


    return {

        "tested_candles":
            len(candles),

        "raw_smart_sweeps":
            len(signals),

        "average_score":
            round(avg,2),

        "premium":
            len(
                [
                    x for x in signals
                    if x["quality"]=="PREMIUM"
                ]
            ),

        "signals":
            signals[-10:]

    }



def liquidity_sweep_final_professional_engine(candles):

    result = liquidity_sweep_smart_money_filter(
        candles
    )


    zones=[]


    for signal in result.get(
        "signals",
        []
    ):


        index=signal["index"]

        level=signal["level"]


        age=len(candles)-index


        if age<=20:

            liquidity_status="FRESH"

        elif age<=100:

            liquidity_status="ACTIVE"

        else:

            liquidity_status="OLD"



        institutional_probability=signal["score"]


        if "DISPLACEMENT" in signal["reasons"]:

            institutional_probability+=5


        if "STRUCTURE SHIFT" in signal["reasons"]:

            institutional_probability+=5


        if institutional_probability>100:

            institutional_probability=100



        zones.append({

            "index":
                index,

            "direction":
                signal["direction"],

            "zone":
                round(
                    level,
                    6
                ),

            "liquidity_status":
                liquidity_status,

            "score":
                signal["score"],

            "institutional_probability":
                institutional_probability,

            "quality":
                (
                    "PREMIUM"
                    if institutional_probability>=90
                    else signal["quality"]
                ),

            "reasons":
                signal["reasons"]

        })



    premium=len(
        [
            z for z in zones
            if z["quality"]=="PREMIUM"
        ]
    )


    return {

        "tested_candles":
            len(candles),

        "signals_found":
            len(zones),

        "premium_signals":
            premium,

        "average_score":
            result.get(
                "average_score"
            ),

        "professional_signals":
            zones

    }



def liquidity_sweep_institutional_decay_engine(candles):

    base = liquidity_sweep_final_professional_engine(
        candles
    )


    filtered=[]


    for signal in base.get(
        "professional_signals",
        []
    ):


        age = len(candles) - signal["index"]


        score = signal["score"]


        # ======================
        # LIQUIDITY DECAY
        # ======================

        if age <= 20:

            status="FRESH"

            score += 10


        elif age <= 100:

            status="ACTIVE"


        elif age <= 150:

            status="OLD"

            score -= 10


        else:

            status="EXPIRED"

            score -= 25



        if score > 100:

            score=100


        if score < 0:

            score=0



        # ======================
        # FINAL QUALITY
        # ======================

        if status=="EXPIRED":

            quality="INVALID"


        elif score>=90:

            quality="PREMIUM"


        elif score>=75:

            quality="HIGH"


        elif score>=60:

            quality="MEDIUM"


        else:

            quality="LOW"



        if quality!="INVALID":

            filtered.append({

                "index":
                    signal["index"],

                "direction":
                    signal["direction"],

                "zone":
                    signal["zone"],

                "liquidity_status":
                    status,

                "institutional_score":
                    score,

                "quality":
                    quality,

                "reasons":
                    signal["reasons"]

            })



    premium=len(
        [
            x for x in filtered
            if x["quality"]=="PREMIUM"
        ]
    )


    avg=0


    if filtered:

        avg=sum(
            x["institutional_score"]
            for x in filtered
        )/len(filtered)



    return {

        "tested_candles":
            len(candles),

        "valid_signals":
            len(filtered),

        "premium_signals":
            premium,

        "average_score":
            round(avg,2),

        "signals":
            filtered

    }

