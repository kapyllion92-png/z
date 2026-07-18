from app.services.historical.database import HistoricalDatabase
from app.services.features.builder import FeatureBuilder


def main():

    db = HistoricalDatabase()

    candles = db.get_candles(
        "BTCUSDT",
        "60",
        100,
    )

    builder = FeatureBuilder()

    features = builder.build(
        candles[::-1]
    )

    print(features)


if __name__ == "__main__":
    main()
