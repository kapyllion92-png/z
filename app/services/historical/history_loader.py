
import requests


class HistoryLoader:
    def __init__(self):
        self.base_url = "https://api.bybit.com"

    def load(self, symbol="BTCUSDT", interval="15", limit=200):
        url = f"{self.base_url}/v5/market/kline"

        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        if data.get("retCode") != 0:
            return []

        candles = data["result"]["list"]

        return candles


    def status(self, symbol="BTCUSDT", interval="15"):
        candles = self.load(symbol, interval)

        return {
            "symbol": symbol,
            "interval": interval,
            "candles": len(candles)
        }
