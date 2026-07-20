from datetime import datetime


class PaperTrader:


    def __init__(self):

        self.balance = 1000

        self.position = None

        self.history = []



    def open_trade(
        self,
        side,
        qty,
        entry,
        stop_loss,
        take_profit
    ):


        self.position = {

            "side": side,

            "qty": qty,

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "time":
                datetime.now().isoformat()

        }


        return self.position



    def check_price(
        self,
        price
    ):


        if not self.position:

            return None



        p = self.position


        result = None



        if p["side"] == "LONG":


            if price >= p["take_profit"]:

                result = "TP"


            elif price <= p["stop_loss"]:

                result = "SL"



        if result:


            profit = (
                price - p["entry"]
            ) * p["qty"]


            self.balance += profit


            trade = {

                "result": result,

                "profit":
                    round(profit,2),

                "price":
                    price,

                "balance":
                    round(self.balance,2)

            }


            self.history.append(trade)

            self.position = None


            return trade



        return {
            "status":
                "OPEN",
            "price":
                price
        }
