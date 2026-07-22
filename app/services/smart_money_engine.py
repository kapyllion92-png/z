from app.services.choch_engine import CHoCHEngine


class SmartMoneyEngine:

    def __init__(self):
        self.choch_engine = CHoCHEngine()


    def analyze(self, candles):

        result = {}

        choch = self.choch_engine.analyze(
            candles=candles,
            volume_ratio=1,
            displacement=True
        )

        result["CHoCH"] = choch

        return result
