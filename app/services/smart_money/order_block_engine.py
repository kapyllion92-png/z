from typing import Dict, List


class OrderBlockEngine:

    def __init__(self):
        self.version = "ORDER BLOCK ENGINE v2.0"


    def analyze(self, candles) -> Dict:

        result = {
            "engine": self.version,
            "order_blocks": [],
            "blocks": [],
            "top_order_blocks": []
        }


        if not candles or len(candles) < 20:
            result["error"] = "NOT ENOUGH DATA"
            return result


        blocks = []


        avg_volume = sum(
            float(c.get("volume", 0))
            for c in candles[-20:]
        ) / 20


        for i in range(5, len(candles)-3):

            c = candles[i]

            op = float(c["open"])
            high = float(c["high"])
            low = float(c["low"])
            close = float(c["close"])
            volume = float(c.get("volume",0))


            body = abs(close-op)
            rng = high-low


            if rng == 0:
                continue


            displacement = body / rng


            future = candles[i+1:i+4]


            future_move = (
                float(future[-1]["close"])
                -
                close
            )


            score = 50
            reasons = []


            direction = None


            # bullish OB
            if close > op and future_move > 0:

                direction="LONG"

                score += 20

                reasons.append(
                    "BULLISH ORDER BLOCK"
                )


            # bearish OB
            elif close < op and future_move < 0:

                direction="SHORT"

                score += 20

                reasons.append(
                    "BEARISH ORDER BLOCK"
                )


            else:
                continue


            # displacement
            if displacement > 0.6:

                score += 10

                reasons.append(
                    "DISPLACEMENT"
                )


            # volume confirmation
            if volume > avg_volume:

                score += 10

                reasons.append(
                    "VOLUME CONFIRMATION"
                )


            # freshness
            freshness = 100


            # reaction strength
            reaction = min(
                100,
                int(abs(future_move) / max(rng,1) * 100)
            )


            score += min(
                10,
                reaction // 10
            )


            quality = "C"

            if score >=90:
                quality="A+"
            elif score >=80:
                quality="A"
            elif score >=70:
                quality="B"


            block = {

                "direction": direction,

                "zone":[
                    round(low,2),
                    round(high,2)
                ],

                "score": min(score,100),

                "quality":quality,

                "freshness":freshness,

                "reaction_strength":reaction,

                "reasons":reasons
            }


            blocks.append(block)



        blocks = sorted(
            blocks,
            key=lambda x:x["score"],
            reverse=True
        )


        unique=[]

        seen=set()


        for b in blocks:

            key=(
                b["direction"],
                tuple(b["zone"])
            )

            if key not in seen:

                seen.add(key)
                unique.append(b)



        result["order_blocks"]=unique[:20]
        result["blocks"]=unique[:20]
        result["top_order_blocks"]=unique[:10]


        if not unique:

            result["error"]="NO ORDER BLOCKS"


        return result



def order_block_engine_v17000(candles):

    return OrderBlockEngine().analyze(candles)



def order_block_engine_v18101(candles):

    return OrderBlockEngine().analyze(candles)
