from app.services.market_analyzer import MarketAnalyzer
from app.services.historical.database import HistoricalDatabase
from app.services.terminal_view import TerminalView


def main():

    db = HistoricalDatabase()

    analyzer = MarketAnalyzer()

    view = TerminalView()

    candles = db.get_candles(
        "BTCUSDT",
        "60",
        100
    )

    result = analyzer.analyze(
        candles[::-1]
    )

    view.show_report(result)


if __name__ == "__main__":
    main()
