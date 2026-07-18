from app.services.bybit.client import BybitClient


class CandleDataEngine:
    def __init__(self):
        self.client = BybitClient()

    def get_candles(self, symbol="BTCUSDT", interval="60", limit=200):
        response = self.client.session.get_kline(
            category="linear",
            symbol=symbol,
            interval=interval,
            limit=limit,
        )

        return response
