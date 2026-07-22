from app.services.exchange.bybit_client import BybitClient


class BybitExecutor:


    def __init__(self):

        self.client = BybitClient()



    def execute_trade(
        self,
        trade
    ):

        order = self.client.create_order(

            symbol=trade["symbol"],

            side=
                "Buy"
                if trade["side"] == "LONG"
                else "Sell",

            qty=trade["qty"],

            price=trade["price"]

        )


        self.client.set_stop_take(

            symbol=trade["symbol"],

            stop_loss=trade["stop_loss"],

            take_profit=trade["take_profit"]

        )


        return order
