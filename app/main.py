from app.services.historical.database import HistoricalDatabase
from app.services.market_analyzer import MarketAnalyzer



def main():

    db = HistoricalDatabase()


    candles = db.get_candles(
        "BTCUSDT",
        "60",
        100,
    )


    analyzer = MarketAnalyzer()


    result = analyzer.analyze(
        candles[::-1]
    )


    print()
    print("=== MARKET FEATURES ===")
    print(result["features"])


    print()
    print("=== STRATEGY ===")
    print(result["strategy"])


    print()
    print("=== MARKET STRUCTURE ===")
    print(result["structure"])


    print()
    print("=== SIGNAL RANKING ===")
    print(result["ranking"])


    print()
    print("=== ENTRY SETUP ===")
    print(result["entry"])


    print()
    print("=== TRADE PLAN ===")
    print(result["trade_plan"])



if __name__ == "__main__":
    main()
