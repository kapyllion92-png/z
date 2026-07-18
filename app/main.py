from app.services.historical.database import HistoricalDatabase
from app.services.features.builder import FeatureBuilder
from app.services.strategies.trend import TrendStrategy
from app.services.ranking.scorer import SignalScorer


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


    ranking = SignalScorer().score(
        features,
        analysis
    )


    print()
    print("=== MARKET FEATURES ===")
    print(features)

    print()
    print("=== STRATEGY ===")
    print(analysis)

    print()
    print("=== SIGNAL RANKING ===")
    print(ranking)



if __name__ == "__main__":
    main()
