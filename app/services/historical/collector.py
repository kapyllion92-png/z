from app.services.market_data.candles import CandleDataEngine
from app.services.market_data.parser import parse_candles
from app.services.historical.database import HistoricalDatabase


class HistoricalCollector:

    def __init__(self):
        self.market = CandleDataEngine()
        self.database = HistoricalDatabase()


    def collect(self, symbol="BTCUSDT", interval="60", limit=200):

        response = self.market.get_candles(
            symbol=symbol,
            interval=interval,
            limit=limit,
        )

        candles = parse_candles(
            response["result"]["list"]
        )

        for candle in candles:
            self.database.save_candle(
                symbol,
                interval,
                candle
            )

        return len(candles)
