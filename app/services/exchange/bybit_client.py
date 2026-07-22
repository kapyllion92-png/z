from app.config.settings import TRADING_MODE


class BybitClient:


    def __init__(self):

        self.mode = TRADING_MODE


    def create_order(
        self,
        symbol,
        side,
        qty,
        price=None
    ):

        if self.mode != "LIVE":

            return {

                "exchange": "BYBIT",

                "mode": self.mode,

                "status": "SIMULATED_ORDER",

                "symbol": symbol,

                "side": side,

                "qty": qty,

                "price": price

            }


        raise Exception(
            "LIVE MODE DISABLED. API KEYS REQUIRED."
        )


    def set_stop_take(
        self,
        symbol,
        stop_loss,
        take_profit
    ):

        return {

            "status":
                "SIMULATED_STOP_TAKE",

            "stop_loss":
                stop_loss,

            "take_profit":
                take_profit

        }
