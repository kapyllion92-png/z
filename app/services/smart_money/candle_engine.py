from typing import Dict, List


class CandleEngine:


    def analyze(self, candles: List[Dict]) -> Dict:


        result = {

            "bullish_engulfing": False,
            "bearish_engulfing": False,

            "pin_bar": False,
            "bullish_pin_bar": False,
            "bearish_pin_bar": False,

            "doji": False,

            "hammer": False,
            "shooting_star": False,

            "inside_bar": False,
            "outside_bar": False,

            "morning_star": False,
            "evening_star": False,

            "three_white_soldiers": False,
            "three_black_crows": False,


            "bullish_candle": False,
            "bearish_candle": False,

            "direction": "NEUTRAL",

            "body_strength": "NORMAL",
            "candle_size": "NORMAL",


            "score": 0,
            "reasons": []

        }


        if len(candles) < 3:
            return result


        prev = candles[-2]
        last = candles[-1]


        o1=float(prev["open"])
        c1=float(prev["close"])
        h1=float(prev["high"])
        l1=float(prev["low"])


        o=float(last["open"])
        c=float(last["close"])
        h=float(last["high"])
        l=float(last["low"])



        body = abs(c-o)
        rng = h-l


        if rng == 0:
            return result


        upper = h-max(o,c)
        lower = min(o,c)-l



        # =====================
        # DIRECTION
        # =====================

        if c > o:

            result["bullish_candle"]=True
            result["direction"]="BULLISH"


        elif c < o:

            result["bearish_candle"]=True
            result["direction"]="BEARISH"



        # =====================
        # BODY STRENGTH
        # =====================

        body_ratio = body/rng


        if body_ratio >= 0.7:

            result["body_strength"]="STRONG"

            result["score"] += 5

            result["reasons"].append(
                "STRONG BODY"
            )


        elif body_ratio < 0.3:

            result["body_strength"]="WEAK"



        # =====================
        # SIZE
        # =====================

        if rng > 0:

            avg = sum(
                float(x["high"])-float(x["low"])
                for x in candles[-10:]
            ) / min(len(candles),10)


            if rng > avg*1.5:

                result["candle_size"]="LARGE"

            elif rng < avg*0.5:

                result["candle_size"]="SMALL"



        # =====================
        # ENGULFING
        # =====================

        if (
            c1 < o1
            and
            c > o
            and
            o <= c1
            and
            c >= o1
        ):

            result["bullish_engulfing"]=True
            result["score"]+=15
            result["reasons"].append(
                "BULLISH ENGULFING"
            )


        if (
            c1 > o1
            and
            c < o
            and
            o >= c1
            and
            c <= o1
        ):

            result["bearish_engulfing"]=True
            result["score"]+=15
            result["reasons"].append(
                "BEARISH ENGULFING"
            )



        # =====================
        # DOJI
        # =====================

        if body/rng <= 0.15:

            result["doji"]=True
            result["score"]+=5

            result["reasons"].append(
                "DOJI"
            )



        # =====================
        # HAMMER
        # =====================

        if (
            lower >= body*2
            and
            upper <= body
        ):

            result["hammer"]=True
            result["bullish_pin_bar"]=True

            result["score"]+=10

            result["reasons"].append(
                "HAMMER"
            )



        # =====================
        # SHOOTING STAR
        # =====================

        if (
            upper >= body*2
            and
            lower <= body
        ):

            result["shooting_star"]=True
            result["bearish_pin_bar"]=True

            result["score"]+=10

            result["reasons"].append(
                "SHOOTING STAR"
            )



        if result["bullish_pin_bar"] or result["bearish_pin_bar"]:

            result["pin_bar"]=True



        # =====================
        # INSIDE BAR
        # =====================

        if (
            h < h1
            and
            l > l1
        ):

            result["inside_bar"]=True

            result["score"]+=10

            result["reasons"].append(
                "INSIDE BAR"
            )



        # =====================
        # OUTSIDE BAR
        # =====================

        if (
            h > h1
            and
            l < l1
        ):

            result["outside_bar"]=True

            result["score"]+=10

            result["reasons"].append(
                "OUTSIDE BAR"
            )



        # =====================
        # 3 CANDLE PATTERNS
        # =====================

        if len(candles)>=3:

            a,b,candle=candles[-3],candles[-2],candles[-1]


            if (
                float(a["close"]) < float(a["open"])
                and
                abs(float(b["close"])-float(b["open"])) < 
                abs(float(a["close"])-float(a["open"]))*0.5
                and
                float(candle["close"]) > float(candle["open"])
                and
                float(candle["close"]) >
                float(a["open"])
            ):

                result["morning_star"]=True
                result["score"]+=20

                result["reasons"].append(
                    "MORNING STAR"
                )



            if (
                float(a["close"]) > float(a["open"])
                and
                abs(float(b["close"])-float(b["open"])) <
                abs(float(a["close"])-float(a["open"]))*0.5
                and
                float(candle["close"]) < float(candle["open"])
                and
                float(candle["close"]) <
                float(a["open"])
            ):

                result["evening_star"]=True
                result["score"]+=20

                result["reasons"].append(
                    "EVENING STAR"
                )


        return result
