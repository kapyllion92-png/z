from app.core.market_config import (
    SYMBOLS,
    INTERVALS,
    DEFAULT_HISTORY_LIMIT,
)

from app.services.historical.collector import HistoricalCollector


class HistoricalLoader:

    def __init__(self):
        self.collector = HistoricalCollector()


    def load_market_history(self):

        total = 0

        for symbol in SYMBOLS:

            for interval in INTERVALS:

                print(
                    f"Loading {symbol} {interval}"
                )

                count = self.collector.collect(
                    symbol=symbol,
                    interval=interval,
                    limit=DEFAULT_HISTORY_LIMIT,
                )

                total += count

                print(
                    f"Saved {count} candles"
                )


        return total
