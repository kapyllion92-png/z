from typing import List, Dict


class SmartMoneyEngine:

    def __init__(self):
        pass


    def order_block(self, candles: List[Dict]) -> Dict:
        if len(candles) < 10:
            return {

                "found": False,
                "type": None,
                "score": 0
            }

        try:
            ob = candles[-3]
            last = candles[-1]

            ob_open = float(ob["open"])
            ob_close = float(ob["close"])
            ob_high = float(ob["high"])
            ob_low = float(ob["low"])

            last_close = float(last["close"])

            body = abs(ob_close - ob_open)
            candle_range = ob_high - ob_low

            if candle_range == 0:
                return {
                    "found": False,
                    "type": None,
                    "score": 0
                }

            strength = body / candle_range

            bullish = (
                ob_close < ob_open
                and last_close > ob_high
                and strength > 0.45
            )

            bearish = (
                ob_close > ob_open
                and last_close < ob_low
                and strength > 0.45
            )

            if bullish:
                return {
                    "found": True,
                    "type": "BULLISH OB",
                    "score": 30
                }

            if bearish:
                return {
                    "found": True,
                    "type": "BEARISH OB",
                    "score": 30
                }

            return {
                "found": False,
                "type": None,
                "score": 0
            }

        except Exception:
            return {
                "found": False,
                "type": None,
                "score": 0
            }


    def liquidity_sweep(self, candles: List[Dict]) -> bool:
        if len(candles) < 5:
            return False

        try:
            prev = candles[-2]
            last = candles[-1]

            return (
                float(last["high"]) > float(prev["high"])
                or
                float(last["low"]) < float(prev["low"])
            )

        except Exception:
            return False


    def stop_hunt(self, candles: List[Dict]) -> bool:
        if len(candles) < 3:
            return False

        try:
            prev = candles[-2]
            last = candles[-1]

            prev_high = float(prev["high"])
            prev_low = float(prev["low"])

            last_high = float(last["high"])
            last_low = float(last["low"])
            last_close = float(last["close"])

            return (
                (last_low < prev_low and last_close > prev_low)
                or
                (last_high > prev_high and last_close < prev_high)
            )

        except Exception:
            return False




    def fair_value_gap(self, candles):
        if len(candles) < 3:
            return False

        try:
            first = candles[-3]
            last = candles[-1]

            first_high = float(first["high"])
            first_low = float(first["low"])

            last_high = float(last["high"])
            last_low = float(last["low"])

            bullish_fvg = last_low > first_high
            bearish_fvg = last_high < first_low

            return bullish_fvg or bearish_fvg

        except Exception:
            return False


    def imbalance(self, candles):
        if len(candles) < 3:
            return False

        try:
            bodies = []

            for c in candles[-3:]:
                bodies.append(
                    abs(
                        float(c["close"]) -
                        float(c["open"])
                    )
                )

            return bodies[1] > (
                (bodies[0] + bodies[2]) / 2
            ) * 1.8

        except Exception:
            return False


    def mitigation_block(self, candles):
        if len(candles) < 5:
            return False

        try:
            block = candles[-5]
            price = float(candles[-1]["close"])

            high = float(block["high"])
            low = float(block["low"])

            return low <= price <= high

        except Exception:
            return False




    def change_of_character(self, candles):
        if len(candles) < 6:
            return False

        try:
            recent = candles[-5:-1]
            last = candles[-1]

            highs = [
                float(c["high"])
                for c in recent
            ]

            lows = [
                float(c["low"])
                for c in recent
            ]

            last_high = float(last["high"])
            last_low = float(last["low"])

            bullish_choch = last_high > max(highs)
            bearish_choch = last_low < min(lows)

            return bullish_choch or bearish_choch

        except Exception:
            return False




    def premium_discount(self, candles):
        """
        Calculate premium/discount location.
        """
        try:
            if len(candles) < 20:
                return None

            highs = [
                float(c["high"])
                for c in candles[-20:]
            ]

            lows = [
                float(c["low"])
                for c in candles[-20:]
            ]

            high = max(highs)
            low = min(lows)

            current = float(candles[-1]["close"])

            equilibrium = low + (high - low) * 0.5

            if current > equilibrium:
                return "PREMIUM"

            return "DISCOUNT"

        except Exception:
            return None



    def advanced_imbalance(self, candles):
        """
        Detect institutional imbalance.
        """
        try:
            if len(candles) < 5:
                return False

            a = candles[-5]
            c = candles[-3]

            a_high = float(a["high"])
            a_low = float(a["low"])

            c_high = float(c["high"])
            c_low = float(c["low"])

            bullish = c_low > a_high
            bearish = c_high < a_low

            return bullish or bearish

        except Exception:
            return False



    def advanced_mitigation_block(self, candles):
        """
        Detect mitigation return into previous block.
        """
        try:
            if len(candles) < 6:
                return False

            block = candles[-5]
            current = candles[-1]

            block_high = float(block["high"])
            block_low = float(block["low"])

            price = float(current["close"])

            return block_low <= price <= block_high

        except Exception:
            return False




    def premium_zone(self, candles):
        try:
            recent = candles[-20:]

            highs = [
                float(c["high"])
                for c in recent
            ]

            lows = [
                float(c["low"])
                for c in recent
            ]

            highest = max(highs)
            lowest = min(lows)

            equilibrium = (highest + lowest) / 2

            price = float(candles[-1]["close"])

            # premium = ??????? ???????? ?????????
            return price > equilibrium

        except Exception:
            return False




    def breaker_block(self, candles):

        try:
            if len(candles) < 5:
                return False

            c1 = candles[-5]
            c2 = candles[-4]
            c3 = candles[-3]

            high1 = float(c1["high"])
            low1 = float(c1["low"])

            high3 = float(c3["high"])
            low3 = float(c3["low"])


            bullish_breaker = (
                low3 < low1 and
                high3 > high1
            )


            bearish_breaker = (
                high3 > high1 and
                low3 < low1
            )


            return bullish_breaker or bearish_breaker


        except Exception:
            return False



    def break_of_structure(self, candles):

        try:

            recent = candles[-5:-1]
            last = candles[-1]


            highs = [
                float(c["high"])
                for c in recent
            ]

            lows = [
                float(c["low"])
                for c in recent
            ]


            last_high = float(last["high"])
            last_low = float(last["low"])


            bullish_bos = last_high > max(highs)

            bearish_bos = last_low < min(lows)


            return bullish_bos or bearish_bos


        except Exception:
            return False




    def ote_zone(self, candles):
        try:
            highs = [float(c["high"]) for c in candles[-20:]]
            lows = [float(c["low"]) for c in candles[-20:]]

            high = max(highs)
            low = min(lows)

            fib62 = high - (high-low)*0.62
            fib79 = high - (high-low)*0.79

            price = float(candles[-1]["close"])

            return fib79 <= price <= fib62

        except Exception:
            return False


    def liquidity_pool(self, candles):
        try:
            highs = [float(c["high"]) for c in candles[-10:]]
            lows = [float(c["low"]) for c in candles[-10:]]

            equal_high = False
            equal_low = False

            for i in range(len(highs)-1):
                if abs(highs[i]-highs[i+1]) < 5:
                    equal_high=True

                if abs(lows[i]-lows[i+1]) < 5:
                    equal_low=True

            return equal_high or equal_low

        except Exception:
            return False


    def inducement(self,candles):
        try:
            recent=candles[-5:]

            highs=[float(x["high"]) for x in recent]
            lows=[float(x["low"]) for x in recent]

            return (
                highs[-1] > max(highs[:-1])
                or lows[-1] < min(lows[:-1])
            )

        except Exception:
            return False


    def internal_structure(self,candles):
        try:

            last=float(candles[-1]["close"])
            prev=float(candles[-2]["close"])

            if last>prev:
                return "BULLISH"

            return "BEARISH"

        except Exception:
            return "UNKNOWN"




    def dynamic_risk(self,candles,signal):

        try:

            highs=[
                float(x["high"])
                for x in candles[-20:]
            ]

            lows=[
                float(x["low"])
                for x in candles[-20:]
            ]

            price=float(candles[-1]["close"])


            if signal=="SHORT":

                sl=max(highs)

                risk=sl-price

                tp=price-(risk*1.8)


            else:

                sl=min(lows)

                risk=price-sl

                tp=price+(risk*1.8)


            return {
                "entry":price,
                "stop_loss":round(sl,2),
                "take_profit":round(tp,2),
                "risk_reward":1.8
            }


        except Exception:

            return {}




    def final_smc_score(self,reasons):

        weights={

            "BOS":15,
            "Change of Character":15,
            "BEARISH OB":15,
            "BULLISH OB":15,
            "Fair Value Gap":10,
            "Imbalance":10,
            "Liquidity Sweep":10,
            "Liquidity Pool":10,
            "Inducement":10,
            "OTE Zone":10,
            "DISCOUNT Zone":5,
            "PREMIUM Zone":5,
            "Institutional Order Flow":10

        }


        score=0


        for r in reasons:

            for key,value in weights.items():

                if key in r:
                    score+=value


        confirmations=len(reasons)


        if score>100:
            score=100


        if score>=85 and confirmations>=5:

            grade="A+ HIGH CONVICTION"

        elif score>=70:

            grade="A SETUP"

        elif score>=55:

            grade="B SETUP"

        else:

            grade="NO TRADE"


        return {
            "score":score,
            "grade":grade,
            "confirmations":confirmations
        }




    def bos(self, candles: List[Dict]) -> bool:

        if len(candles) < 5:
            return False

        highs=[
            float(c["high"])
            for c in candles[-5:]
        ]

        lows=[
            float(c["low"])
            for c in candles[-5:]
        ]

        last=float(candles[-1]["close"])

        return (
            last > max(highs[:-1])
            or
            last < min(lows[:-1])
        )


    def choch(self, candles: List[Dict]) -> bool:

        if len(candles)<10:
            return False

        return (
            float(candles[-1]["close"])
            !=
            float(candles[-10]["close"])
        )


    def confluence_score(self, candles: List[Dict]) -> Dict:
        """
        FINAL SMC CONFLUENCE MATRIX
        """

        score = 0
        reasons = []

        if len(candles) < 20:
            return {
                "score": 0,
                "reasons": []
            }


        # BOS
        if self.bos(candles):
            score += 10
            reasons.append("BOS CONFIRMED")


        # CHOCH
        if self.change_of_character(candles):
            score += 10
            reasons.append("CHoCH CONFIRMED")


        # ORDER BLOCK
        ob = self.order_block(candles)

        if ob.get("found"):
            score += 15
            reasons.append("ORDER BLOCK CONFIRMED")


        # FVG
        if self.fair_value_gap(candles):
            score += 10
            reasons.append("FVG CONFIRMED")


        # IMBALANCE
        if self.imbalance(candles):
            score += 10
            reasons.append("IMBALANCE CONFIRMED")


        # MITIGATION
        if self.mitigation_block(candles):
            score += 10
            reasons.append("MITIGATION BLOCK")


        # LIQUIDITY
        if self.liquidity_pool(candles):
            score += 10
            reasons.append("LIQUIDITY POOL")


        # INDUCEMENT
        if self.inducement(candles):
            score += 5
            reasons.append("INDUCEMENT")


        # DISCOUNT / PREMIUM
        if self.discount_zone(candles):
            score += 5
            reasons.append("DISCOUNT ENTRY")


        if self.premium_zone(candles):
            score += 5
            reasons.append("PREMIUM ENTRY")


        return {
            "score": min(score,100),
            "reasons": reasons
        }



    def entry_validation(self, candles: List[Dict]) -> Dict:

        conf = self.confluence_score(candles)


        if conf["score"] >= 80:

            return {
                "status":"VALID",
                "confidence":90,
                "reason":"HIGH CONFLUENCE ENTRY",
                "score":conf["score"]
            }


        elif conf["score"] >= 60:

            return {
                "status":"VALID",
                "confidence":70,
                "reason":"MEDIUM CONFLUENCE ENTRY",
                "score":conf["score"]
            }


        else:

            return {
                "status":"WAIT",
                "confidence":40,
                "reason":"LOW CONFLUENCE",
                "score":conf["score"]
            }




    def liquidity_target(self, candles: List[Dict]) -> Dict:

        highs = [
            float(c["high"]) 
            for c in candles[-20:]
        ]

        lows = [
            float(c["low"]) 
            for c in candles[-20:]
        ]


        return {
            "buy_side_liquidity": max(highs),
            "sell_side_liquidity": min(lows)
        }



    def risk_model(self, candles: List[Dict], direction="SHORT") -> Dict:

        last = float(candles[-1]["close"])

        atr = abs(
            float(candles[-1]["high"]) -
            float(candles[-1]["low"])
        )


        if direction == "SHORT":

            stop = last + atr * 2
            target = last - atr * 3


        else:

            stop = last - atr * 2
            target = last + atr * 3



        risk = abs(stop-last)
        reward = abs(last-target)


        rr = round(
            reward/risk,
            2
        ) if risk else 0



        return {

            "entry": last,
            "stop_loss": round(stop,2),
            "take_profit": round(target,2),
            "risk_reward": rr

        }



    def final_entry_model(self, candles: List[Dict]) -> Dict:


        conf = self.confluence_score(candles)

        risk = self.risk_model(
            candles,
            "SHORT"
        )


        validation = self.entry_validation(
            candles
        )


        final_engine = {
            "smc_score": conf["score"],
            "confluences": conf["reasons"],
            "validation": validation,
            "risk_model": risk
        }

        sniper = self.sniper_entry(
            candles,
            final_engine
        )

        final_engine["sniper"] = sniper


        execution = self.execution_filter(
            candles,
            final_engine
        )

        final_engine["execution"] = execution


        gate = self.institutional_gate(
            final_engine
        )

        final_engine["institutional_gate"] = gate



        if gate["allowed"]:

            final_status = "INSTITUTIONAL_ENTRY"

        elif execution["status"] == "WAIT_CONFIRMATION":

            final_status = "WAIT_CONFIRMATION"

        else:

            final_status = "NO_TRADE"



        final_engine["FINAL_STATUS"] = final_status


        return final_engine




    def discount_zone(self, candles: List[Dict]) -> bool:

        if len(candles)<20:
            return False

        highs=[
            float(c["high"])
            for c in candles[-20:]
        ]

        lows=[
            float(c["low"])
            for c in candles[-20:]
        ]

        high=max(highs)
        low=min(lows)

        mid=(high+low)/2

        price=float(candles[-1]["close"])


        return price < mid



    def premium_zone(self, candles: List[Dict]) -> bool:

        if len(candles)<20:
            return False


        highs=[
            float(c["high"])
            for c in candles[-20:]
        ]

        lows=[
            float(c["low"])
            for c in candles[-20:]
        ]


        high=max(highs)
        low=min(lows)

        mid=(high+low)/2

        price=float(candles[-1]["close"])


        return price > mid



    def equilibrium(self, candles: List[Dict]) -> float:

        highs=[
            float(c["high"])
            for c in candles[-20:]
        ]

        lows=[
            float(c["low"])
            for c in candles[-20:]
        ]


        return (
            max(highs)+min(lows)
        )/2



    def poi_zone(self, candles: List[Dict]) -> Dict:

        eq=self.equilibrium(candles)

        return {

            "equilibrium": eq,

            "zone":
            "DISCOUNT"
            if self.discount_zone(candles)
            else
            "PREMIUM"

        }




    def sniper_entry(self, candles: List[Dict], final_engine: Dict) -> Dict:

        confidence=final_engine.get(
            "validation",
            {}
        ).get(
            "confidence",
            0
        )


        confirmations=[]


        if self.bos(candles):
            confirmations.append(
                "BOS"
            )


        if self.choch(candles):
            confirmations.append(
                "CHoCH"
            )


        ob=self.order_block(candles)

        if ob.get("found"):
            confirmations.append(
                "ORDER BLOCK"
            )


        if self.discount_zone(candles):
            confirmations.append(
                "DISCOUNT POI"
            )


        last=float(
            candles[-1]["close"]
        )

        prev=float(
            candles[-2]["close"]
        )


        displacement=abs(
            last-prev
        )


        if displacement > 0:
            confirmations.append(
                "DISPLACEMENT"
            )


        score=len(confirmations)*15


        if score>=75:

            status="SNIPER READY"

        elif score>=50:

            status="WATCH"

        else:

            status="WAIT"


        return {

            "status":status,

            "confidence":
                min(
                    score,
                    100
                ),

            "confirmations":
                confirmations,

            "entry_trigger":
                "ACTIVE"
                if score>=50
                else
                "NONE"

        }




    def execution_filter(self, candles: List[Dict], final_engine: Dict) -> Dict:

        score = final_engine.get(
            "smc_score",
            0
        )

        sniper = final_engine.get(
            "sniper",
            {}
        )

        confidence = sniper.get(
            "confidence",
            0
        )

        last = candles[-1]

        body = abs(
            float(last["close"]) -
            float(last["open"])
        )

        candle_range = (
            float(last["high"]) -
            float(last["low"])
        )

        displacement = False

        if candle_range > 0:
            displacement = (
                body / candle_range
            ) > 0.65


        checks = {

            "SMC_SCORE":
                score >= 70,

            "SNIPER_CONFIDENCE":
                confidence >= 70,

            "DISPLACEMENT":
                displacement,

            "RISK_MODEL":
                "risk_model" in final_engine

        }


        passed = sum(
            1 for x in checks.values()
            if x
        )


        if passed >= 3:

            status = "SNIPER_READY"

        elif passed == 2:

            status = "WAIT_CONFIRMATION"

        else:

            status = "NO_TRADE"


        return {

            "status": status,

            "checks": checks,

            "passed": passed,

            "execution_score":
                passed * 25

        }




    def institutional_gate(self, final_engine: Dict) -> Dict:

        execution = final_engine.get(
            "execution",
            {}
        )

        sniper = final_engine.get(
            "sniper",
            {}
        )


        confirmations = len(
            sniper.get(
                "confirmations",
                []
            )
        )


        execution_score = execution.get(
            "execution_score",
            0
        )


        if (
            execution_score >= 75
            and confirmations >= 4
        ):

            status="INSTITUTIONAL_ENTRY"

        elif execution_score >= 50:

            status="WAIT_CONFIRMATION"

        else:

            status="BLOCKED"


        return {

            "status":status,

            "confirmations":
                confirmations,

            "execution_score":
                execution_score,

            "allowed":
                status=="INSTITUTIONAL_ENTRY"

        }


    def analyze(self, candles: List[Dict]):

        score = 0
        reasons = []

        ob = self.order_block(candles)

        risk_plan = self.dynamic_risk(
            "SHORT" if self.internal_structure(candles)=="BEARISH" else "LONG",
            candles
        )



        if self.ote_zone(candles):
            score += 15
            reasons.append("OTE Zone")

        if self.liquidity_pool(candles):
            score += 10
            reasons.append("Liquidity Pool")

        if self.inducement(candles):
            score += 10
            reasons.append("Inducement")

        structure=self.internal_structure(candles)

        reasons.append(
            "Internal Structure "+structure
        )




        if self.breaker_block(candles):
            score += 15
            reasons.append("Breaker Block")


        if self.break_of_structure(candles):
            score += 20
            reasons.append("BOS")

        if self.mitigation_block(candles):
            score += 15
            reasons.append("Mitigation Block")

        if self.imbalance(candles):
            score += 15
            reasons.append("Imbalance")

        if self.premium_zone(candles):
            score += 10
            reasons.append("PREMIUM Zone")

        zone = self.premium_discount(candles)

        if self.advanced_imbalance(candles):
            score += 15
            reasons.append("Imbalance")

        if self.advanced_mitigation_block(candles):
            score += 15
            reasons.append("Mitigation Block")

        if zone:
            reasons.append(zone + " Zone")

        if self.imbalance(candles):
            score += 15
            reasons.append("Imbalance")

        if self.mitigation_block(candles):
            score += 15
            reasons.append("Mitigation Block")


        if self.change_of_character(candles):
            score += 20
            reasons.append("Change of Character")

        if self.fair_value_gap(candles):
            score += 15
            reasons.append("Fair Value Gap")


        if self.imbalance(candles):
            score += 15
            reasons.append("Imbalance")


        if self.mitigation_block(candles):
            score += 15
            reasons.append("Mitigation Block")

        if self.imbalance(candles):
            score += 15
            reasons.append("Imbalance")

        if self.mitigation_block(candles):
            score += 15
            reasons.append("Mitigation Block")

        if self.liquidity_sweep(candles):
            score += 20
            reasons.append("Liquidity Sweep")

        if self.stop_hunt(candles):
            score += 20
            reasons.append("Stop Hunt")

        if ob["found"]:
            score += ob["score"]
            reasons.append(ob["type"])

        if ob.get("found"):
            score += 10
            reasons.append("Institutional Order Flow")

        if score >= 80:
            reasons.append("HIGH CONVICTION SMART MONEY")

        score = min(score, 100)

        return {
            "score": score,
            "reasons": reasons,
            "order_block": ob
        }