from typing import Dict


def entry_quality_engine(candles, smart_money=None):

    current_price = float(candles[-1]["close"])

    if smart_money is None:
        return {
            "engine": "ENTRY QUALITY ENGINE v17000",
            "error": "NO SMART MONEY"
        }


    order_block = smart_money.get("order_block", {})

    blocks = (
        order_block.get("top_order_blocks")
        or order_block.get("order_blocks")
        or []
    )


    if not blocks:
        return {
            "engine":"ENTRY QUALITY ENGINE v17000",
            "error":"NO ORDER BLOCKS",
            "current_price":current_price
        }


    setups=[]


    for block in blocks:

        direction = block.get("direction")
        zone = block.get("zone")

        if not zone:
            continue


        low=float(zone[0])
        high=float(zone[1])

        distance = abs(current_price - ((low+high)/2)) / current_price * 100


        score = int(block.get("score",0))

        reasons=list(block.get("reasons",[]))


        if direction=="LONG":

            if high < current_price:
                continue

            if low <= current_price <= high:
                reasons.append("NEAR ENTRY")
                score +=10


        if direction=="SHORT":

            if low > current_price:
                pass

            if low <= current_price <= high:
                reasons.append("NEAR ENTRY")
                score +=10


        location="DISCOUNT" if direction=="LONG" else "PREMIUM"


        setups.append({

            "direction":direction,

            "zone":[low,high],

            "score":min(score,100),

            "quality":
                "A+" if score>=90
                else "A" if score>=80
                else "B",

            "distance":round(distance,2),

            "location":location,

            "reasons":reasons
        })


    if not setups:

        return {
            "engine":"ENTRY QUALITY ENGINE v17000",
            "error":"NO VALID ENTRY ZONE",
            "current_price":current_price
        }


    setups=sorted(
        setups,
        key=lambda x:x["score"],
        reverse=True
    )


    best=setups[0]


    # запрещаем вход против текущей зоны

    if best["direction"]=="SHORT":

        if current_price < best["zone"][0]:

            best["status"]="WAIT_FOR_PULLBACK"

    if best["direction"]=="LONG":

        if current_price > best["zone"][1]:

            best["status"]="WAIT_FOR_PULLBACK"


    return {

        "engine":"ENTRY QUALITY ENGINE v17000",

        "current_price":current_price,

        "best_setup":best,

        "setups":setups[:10]
    }
