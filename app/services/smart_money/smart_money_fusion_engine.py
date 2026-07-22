from app.services.smart_money.order_block_engine import order_block_engine_v17000
from app.services.smart_money.choch_engine import CHoCHEngine


class SmartMoneyFusionEngine:


    def __init__(self):

        self.choch_engine = CHoCHEngine()



    def analyze(self, candles, volume_ratio=1.0):


        if not candles or len(candles) < 20:

            return {

                "engine":
                    "SMART MONEY FUSION v4.0",

                "ready":
                    False,

                "reason":
                    "NOT ENOUGH DATA"

            }



        # ORDER BLOCK ENGINE

        ob = order_block_engine_v17000(
            candles
        )


        blocks = ob.get(
            "top_order_blocks",
            []
        )


        best_setup = {}


        if blocks:

            best_setup = max(
                blocks,
                key=lambda x: x.get(
                    "score",
                    0
                )
            )



        # CHoCH ENGINE

        choch = self.choch_engine.analyze(

            candles,

            volume_ratio,

            blocks

        )



        fusion_score = choch.get(
            "score",
            0
        )


        ready = (

            choch.get("choch") != "NONE"

            and fusion_score >= 70

            and bool(best_setup)

        )



        return {


            "engine":

                "SMART MONEY FUSION v4.0",


            "ready":

                ready,


            "fusion_score":

                fusion_score,


            "order_block":

                ob,


            "choch":

                choch,


            "best_setup":

                best_setup,


            "setups":

                blocks

        }



def smart_money_analysis(

    candles,

    volume_ratio=1.0

):

    engine = SmartMoneyFusionEngine()


    return engine.analyze(

        candles,

        volume_ratio

    )
