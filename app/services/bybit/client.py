from pybit.unified_trading import HTTP

from app.core.security.secrets import BYBIT_API_KEY, BYBIT_API_SECRET


class BybitClient:
    def __init__(self):
        self.session = HTTP(
            testnet=True,
            api_key=BYBIT_API_KEY,
            api_secret=BYBIT_API_SECRET,
        )

    def get_status(self):
        return "Bybit API client ready"
