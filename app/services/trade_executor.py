class TradeExecutor:


    def __init__(self):
        self.status = "READY"



    def prepare(
        self,
        trade_plan
    ):

        if not trade_plan:

            return {

                "status":
                    "NO_TRADE",

                "message":
                    "Trade plan missing"

            }



        side = trade_plan.get(
            "side"
        )


        if side not in [
            "LONG",
            "SHORT"
        ]:

            return {

                "status":
                    "INVALID",

                "message":
                    "Invalid trade side"

            }



        execution = {


            "status":
                "READY",


            "side":
                side,


            "entry":
                trade_plan.get(
                    "entry"
                ),


            "stop_loss":
                trade_plan.get(
                    "stop_loss"
                ),


            "take_profit":
                trade_plan.get(
                    "take_profit"
                ),


            "position_size":
                trade_plan.get(
                    "position_size"
                ),


            "risk_reward":
                trade_plan.get(
                    "risk_reward"
                ),


            "mode":
                "SIMULATION"

        }


        return execution
