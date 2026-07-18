from app.services.historical.loader import HistoricalLoader


def main():

    loader = HistoricalLoader()

    total = loader.load_market_history()

    print(
        "Total candles saved:",
        total
    )


if __name__ == "__main__":
    main()
