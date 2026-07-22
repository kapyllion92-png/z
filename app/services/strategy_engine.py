from app.services.strategies.bounce import BounceStrategy
from app.services.strategies.breakout import BreakoutStrategy
from app.services.strategies.fake_breakout import FakeBreakoutStrategy
from app.services.strategies.volume import VolumeStrategy
from app.services.strategies.imbalance import ImbalanceStrategy
from app.services.strategies.range_break import RangeBreakStrategy


class StrategyEngine:

    def __init__(self):

        self.strategies = [
            BounceStrategy(),
            BreakoutStrategy(),
            FakeBreakoutStrategy(),
            VolumeStrategy(),
            ImbalanceStrategy(),
            RangeBreakStrategy()
        ]


    def analyze(self, features):

        total_score = 0
        signals = []
        reasons = []
        strategy_names = []


        names = {

            "BOUNCE":
                "Отбой от уровня",

            "BREAKOUT":
                "Пробой ключевого уровня",

            "FAKE_BREAKOUT":
                "Ложный пробой с возвратом",

            "RANGE_BREAK":
                "Выход из зоны консолидации",

            "IMBALANCE":
                "Дисбаланс спроса и предложения",

            "VOLUME":
                "Объёмное подтверждение движения"
        }


        for strategy in self.strategies:

            result = strategy.analyze(features)


            if result.get("score", 0) > 0:

                total_score += result["score"]


                if result.get("strategy"):

                    code = result["strategy"]

                    strategy_names.append(
                        names.get(code, code)
                    )


                for r in result.get("reasons", []):

                    if "BREAK" in r:
                        reasons.append(
                            "Пробой важного уровня"
                        )

                    elif "VOLUME" in r:
                        reasons.append(
                            "Объём подтвердил движение"
                        )

                    elif "IMBALANCE" in r:
                        reasons.append(
                            "Сформирован дисбаланс покупателей и продавцов"
                        )

                    elif "RANGE" in r:
                        reasons.append(
                            "Цена вышла из зоны накопления"
                        )

                    elif "PRESSURE" in r:
                        reasons.append(
                            "Усиление давления участников рынка"
                        )


            if result.get("signal") not in [
                "NONE",
                "WAIT",
                None
            ]:

                signals.append(
                    result["signal"]
                )


        long_count = signals.count("LONG")
        short_count = signals.count("SHORT")


        if long_count > short_count:

            final_signal = "LONG"

        elif short_count > long_count:

            final_signal = "SHORT"

        else:

            final_signal = "WAIT"



        unique_strategies = list(set(strategy_names))


        return {

            "signal":
                final_signal,

            "score":
                min(total_score, 100),

            "strategy_name":
                ", ".join(unique_strategies)
                if unique_strategies
                else "Комплексный сигнал",

            "strategies":
                unique_strategies,

            "reasons":
                list(set(reasons))
        }
