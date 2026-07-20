class Signal:


    def __init__(
        self,
        symbol,
        direction,
        strength,
        setup,
        reasons,
        entry=None,
        stop=None,
        target=None,
        profit=None,
        decision=None,
        waiting=None
    ):


        self.symbol = symbol

        self.direction = direction

        self.strength = strength

        self.setup = setup

        self.reasons = reasons

        self.entry = entry

        self.stop = stop

        self.target = target

        self.profit = profit

        self.decision = decision

        self.waiting = waiting



    def to_dict(self):


        return {


            "монета":
            self.symbol,


            "направление":
            self.direction,


            "стратегия":
            self.setup,


            "сила":
            self.strength,


            "причины":
            self.reasons,


            "вход":
            self.entry,


            "стоп":
            self.stop,


            "тейк":
            self.target,


            "прибыль":
            self.profit,


            "решение":
            self.decision,


            "ожидание":
            self.waiting

        }
