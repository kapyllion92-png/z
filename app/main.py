from app.services.historical.collector import HistoricalCollector
from app.services.historical.database import HistoricalDatabase


def main():

    collector = HistoricalCollector()

    saved = collector.collect(
        symbol="BTCUSDT",
        interval="60",
        limit=200,
    )

    print("Saved candles:", saved)


    database = HistoricalDatabase()

    history = database.get_candles(
        "BTCUSDT",
        "60",
        5,
    )

    print(history)


if __name__ == "__main__":
    main()
