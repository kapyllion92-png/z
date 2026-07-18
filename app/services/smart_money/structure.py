from app.services.smart_money.pivot import PivotDetector
from app.services.smart_money.bos import BOSEngine
from app.services.smart_money.choch import CHoCHEngine
from app.services.smart_money.liquidity import LiquidityEngine
from app.services.smart_money.sweep import SweepDetector
from app.services.smart_money.order_block import OrderBlockDetector



class StructureAnalyzer:


    def __init__(self):

        self.pivot = PivotDetector()

        self.bos = BOSEngine()

        self.choch = CHoCHEngine()

        self.liquidity = LiquidityEngine()

        self.sweep = SweepDetector()

        self.order_block = OrderBlockDetector()



    def analyze(
        self,
        candles
    ):


        pivot_highs, pivot_lows = self.pivot.find_pivots(
            candles
        )


        bos_result = self.bos.analyze(
            candles,
            pivot_highs,
            pivot_lows,
        )


        choch_result = self.choch.analyze(
            candles,
            pivot_highs,
            pivot_lows,
        )


        liquidity_result = self.liquidity.analyze(
            pivot_highs,
            pivot_lows,
        )


        sweep_result = self.sweep.analyze(
            candles,
            liquidity_result,
        )


        order_block_result = self.order_block.analyze(
            candles
        )



        return {


            **bos_result,

            **choch_result,

            **liquidity_result,

            **sweep_result,

            **order_block_result,



            "last_pivot_high":

                pivot_highs[-1]
                if pivot_highs
                else None,


            "last_pivot_low":

                pivot_lows[-1]
                if pivot_lows
                else None,


            "pivot_highs":

                pivot_highs,


            "pivot_lows":

                pivot_lows,

        }
