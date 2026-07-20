from app.services.market_analyzer import MarketAnalyzer
from app.services.historical.database import HistoricalDatabase


def main():

    db = HistoricalDatabase()

    analyzer = MarketAnalyzer()

    candles = db.get_candles(
        "BTCUSDT",
        "60",
        100
    )

    result = analyzer.analyze(
        candles[::-1]
    )


    print()
    print("=== MARKET FEATURES ===")
    print(result.get("features"))


    print()
    print("=== SMART MONEY ===")
    print(result.get("smart_money"))


    print()
    print("=== STRATEGY ===")
    print(result.get("strategy"))


    print()
    print("=== MARKET STRUCTURE ===")
    print(result.get("structure"))


    print()
    print("=== SIGNAL RANKING ===")
    print(result.get("ranking"))


    print()
    print("=== ENTRY SETUP ===")
    print(result.get("entry"))


    print()
    print("=== TRADE PLAN ===")
    print(result.get("trade_plan"))



if __name__ == "__main__":
    main()
