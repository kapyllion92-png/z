from app.services.historical.database import HistoricalDatabase
from app.services.features.builder import FeatureBuilder
from app.services.strategies.trend import TrendStrategy


def main():

    db = HistoricalDatabase()

    candles = db.get_candles(
        "BTCUSDT",
        "60",
        100,
    )

    features = FeatureBuilder().build(
        candles[::-1]
    )


    analysis = TrendStrategy().analyze(
        features
    )


    print(features)
    print(analysis)


if __name__ == "__main__":
    main()
