class BybitSimulator:


    def __init__(self):

        self.exchange = "BYBIT"
        self.mode = "SIMULATION"



    def execute(
        self,
        execution
    ):


        if not execution:

            return {

                "status":
                    "REJECTED",

                "reason":
                    "Empty execution"

            }



        if execution.get("status") != "READY":

            return {

                "status":
                    "REJECTED",

                "reason":
                    "Execution not ready"

            }



        order = {


            "exchange":
                self.exchange,


            "mode":
                self.mode,


            "side":
                execution.get(
                    "side"
                ),


            "entry":
                execution.get(
                    "entry"
                ),


            "stop_loss":
                execution.get(
                    "stop_loss"
                ),


            "take_profit":
                execution.get(
                    "take_profit"
                ),


            "quantity":
                execution.get(
                    "position_size"
                ),


            "risk_reward":
                execution.get(
                    "risk_reward"
                ),


            "status":
                "ORDER_CREATED"

        }


        return order
