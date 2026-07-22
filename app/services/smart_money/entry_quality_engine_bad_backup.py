def entry_quality_engine_v16200(candles):

    from app.services.smart_money.order_block_engine import order_block_engine_v17000


    ob_result = order_block_engine_v17000(candles)

    blocks = ob_result.get(
        "top_order_blocks",
        []
    )


    current = candles[-1]`n`n    if isinstance(current, dict):`n        current_price = float(current["close"])`n    else:`n        current_price = float(current[4])


    if not blocks:
        return {
            "engine":"ENTRY QUALITY ENGINE v16200",
            "error":"NO ORDER BLOCKS",
            "current_price":current_price
        }


    equilibrium = ob_result.get(
        "equilibrium",
        current_price
    )


    setups=[]


    for b in blocks:

        zone=b.get("zone")

        if not zone:
            continue


        low=float(zone[0])
        high=float(zone[1])

        center=(low+high)/2


        distance=abs(
            current_price-center
        )


        distance_percent=round(
            distance/current_price*100,
            2
        )


        score=int(
            b.get(
                "score",
                0
            )
        )


        reasons=list(
            b.get(
                "reasons",
                []
            )
        )


        location=(

            "DISCOUNT"
            if center < equilibrium

            else

            "PREMIUM"

        )


        direction=b.get(
            "direction"
        )


        if direction=="LONG":

            if location=="DISCOUNT":

                score+=10

                reasons.append(
                    "DISCOUNT LONG"
                )

            else:

                score-=5

                reasons.append(
                    "PREMIUM LONG"
                )


        if direction=="SHORT":

            if location=="PREMIUM":

                score+=10

                reasons.append(
                    "PREMIUM SHORT"
                )

            else:

                score-=5

                reasons.append(
                    "DISCOUNT SHORT"
                )


        if distance_percent <= 0.5:

            score+=10

            reasons.append(
                "NEAR ENTRY"
            )


        score=max(
            0,
            min(score,100)
        )


        quality=(

            "A+"

            if score>=90

            else

            "A"

            if score>=80

            else

            "B"

        )


        setups.append({

            "direction":
            direction,

            "zone":
            zone,

            "score":
            score,

            "quality":
            quality,

            "distance":
            distance_percent,

            "location":
            location,

            "reasons":
            reasons

        })


    setups=sorted(
        setups,
        key=lambda x:x["score"],
        reverse=True
    )


    return {

        "engine":
        "ENTRY QUALITY ENGINE v16200",

        "current_price":
        current_price,

        "best_setup":
        setups[0],

        "setups":
        setups[:10]

    }
