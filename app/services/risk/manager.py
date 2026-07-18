class RiskManager:


    def __init__(
        self,
        balance=1000,
        risk_percent=1
    ):

        self.balance = balance
        self.risk_percent = risk_percent



    def calculate(
        self,
        entry,
        stop_loss,
        take_profit,
        side
    ):


        risk_amount = (
            self.balance *
            self.risk_percent /
            100
        )


        distance = abs(
            entry - stop_loss
        )


        if distance == 0:

            return {
                "error": "Invalid stop distance"
            }



        position_size = (
            risk_amount /
            distance
        )


        reward = abs(
            take_profit - entry
        )


        risk_reward = (
            reward /
            distance
        )



        return {

            "side": side,

            "entry": round(
                entry,
                2
            ),

            "stop_loss": round(
                stop_loss,
                2
            ),

            "take_profit": round(
                take_profit,
                2
            ),

            "account_balance":
                self.balance,

            "risk_percent":
                self.risk_percent,

            "risk_amount": round(
                risk_amount,
                2
            ),

            "position_size": round(
                position_size,
                6
            ),

            "risk_reward": round(
                risk_reward,
                2
            ),

        }
