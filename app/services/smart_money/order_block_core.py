def order_block_core_v14900(candles):

    data=[]

    for c in candles:

        try:

            data.append({

                "open":float(c["open"]),
                "high":float(c["high"]),
                "low":float(c["low"]),
                "close":float(c["close"]),
                "volume":float(c.get("volume",0))

            })

        except:

            continue


    blocks=[]


    avg_volume=sum(
        x["volume"] for x in data
    )/len(data) if data else 0



    for i in range(5,len(data)-5):


        ob=data[i-2]

        impulse=data[i-1]

        confirm=data[i+1]



        rng=impulse["high"]-impulse["low"]


        if rng<=0:
            continue



        body=abs(
            impulse["close"]-
            impulse["open"]
        )

        displacement=body/rng



        volume_ok=(
            impulse["volume"]>=avg_volume
        )



        # BULLISH


        if (

            ob["close"] < ob["open"]

            and

            impulse["close"] > ob["high"]

        ):


            score=60


            reasons=[
                "BULLISH ORDER BLOCK"
            ]



            if displacement>=0.25:

                score+=15

                reasons.append(
                    "STRONG DISPLACEMENT"
                )



            if volume_ok:

                score+=10

                reasons.append(
                    "VOLUME CONFIRMATION"
                )



            if confirm["low"]<=ob["high"]:

                score+=10

                reasons.append(
                    "MITIGATION"
                )



            blocks.append({

                "direction":"LONG",

                "zone":[
                    round(ob["low"],2),
                    round(ob["high"],2)
                ],

                "confidence":
                min(score,95),

                "reasons":
                reasons

            })





        # BEARISH


        elif (

            ob["close"] > ob["open"]

            and

            impulse["close"] < ob["low"]

        ):


            score=60


            reasons=[
                "BEARISH ORDER BLOCK"
            ]



            if displacement>=0.25:

                score+=15

                reasons.append(
                    "STRONG DISPLACEMENT"
                )



            if volume_ok:

                score+=10

                reasons.append(
                    "VOLUME CONFIRMATION"
                )



            if confirm["high"]>=ob["low"]:

                score+=10

                reasons.append(
                    "MITIGATION"
                )



            blocks.append({

                "direction":"SHORT",

                "zone":[
                    round(ob["low"],2),
                    round(ob["high"],2)
                ],

                "confidence":
                min(score,95),

                "reasons":
                reasons

            })



    return blocks
