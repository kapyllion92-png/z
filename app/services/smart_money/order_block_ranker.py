from app.services.smart_money.order_block_engine import order_block_engine_v17000


def order_block_engine_v15900(candles):

    result=order_block_engine_v17000(candles)


    blocks=result.get(
        "top_order_blocks",
        []
    )


    ranked=[]


    for b in blocks:

        score=b["score"]

        direction=b["direction"]
        location=b["location"]


        smart_money_bonus=0


        if direction=="LONG":

            if location=="DISCOUNT":
                smart_money_bonus+=10

            else:
                smart_money_bonus-=10


        if direction=="SHORT":

            if location=="PREMIUM":
                smart_money_bonus+=10

            else:
                smart_money_bonus-=10


        final_score=max(
            0,
            min(
                100,
                score+smart_money_bonus
            )
        )


        b["institutional_rank"]=final_score


        if final_score>=90:
            b["quality"]="A+ INSTITUTIONAL"
        elif final_score>=80:
            b["quality"]="A INSTITUTIONAL"
        else:
            b["quality"]="B INSTITUTIONAL"


        ranked.append(b)


    ranked=sorted(
        ranked,
        key=lambda x:x["institutional_rank"],
        reverse=True
    )


    return {

        "engine":
        "ORDER BLOCK INSTITUTIONAL v15900",

        "tested_candles":
        result["tested_candles"],

        "equilibrium":
        result["equilibrium"],

        "top_order_blocks":
        ranked[:5]
    }
