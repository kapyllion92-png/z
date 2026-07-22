import json
import os

class PaperTradingEngine:

    def __init__(self):

        self.account_file = "app/data/account.json"

        if not os.path.exists(self.account_file):

            self.save({
                "mode":"PAPER",
                "balance":10000,
                "position":None
            })


    def load(self):

        with open(self.account_file,"r",encoding="utf-8-sig") as f:
            return json.load(f)


    def save(self,data):

        with open(self.account_file,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=4)


    def open_position(self,trade):

        account=self.load()

        account["position"]={

            "side":trade["side"],
            "qty":trade["qty"],
            "entry":trade["price"],
            "stop_loss":trade["stop_loss"],
            "take_profit":trade["take_profit"],
            "time":trade.get("time",""),
            "status":"OPEN"

        }

        self.save(account)

        return account["position"]


    def close_position(self):

        account=self.load()

        account["position"]=None

        self.save(account)


    def check_position(self,price):

        account=self.load()

        position=account.get("position")

        if position is None:

            return {
                "status":"NONE"
            }

        side=position["side"]

        if side=="LONG":

            if price<=position["stop_loss"]:

                self.close_position()

                return {"status":"STOP"}

            if price>=position["take_profit"]:

                self.close_position()

                return {"status":"TAKE"}

        if side=="SHORT":

            if price>=position["stop_loss"]:

                self.close_position()

                return {"status":"STOP"}

            if price<=position["take_profit"]:

                self.close_position()

                return {"status":"TAKE"}

        return {
            "status":"OPEN",
            "position":position,
            "current_price":price
        }

