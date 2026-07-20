import requests
import json
import os
import time
from datetime import datetime


BYBIT_URL = "https://api.bybit.com/v5/market/kline"

SYMBOL_FILE = "data/markets/bybit_symbols.json"

OUTPUT_DIR = "data/candles"


TIMEFRAMES = {
    "5m": "5",
    "15m": "15",
    "1h": "60",
    "4h": "240",
    "1d": "D"
}


LIMIT = 500


def load_symbols():

    with open(
        SYMBOL_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    return [
        x["symbol"]
        for x in data["symbols"]
    ]



def get_candles(symbol, interval):

    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": interval,
        "limit": LIMIT
    }


    r = requests.get(
        BYBIT_URL,
        params=params,
        timeout=15
    )


    data = r.json()


    if data["retCode"] != 0:
        return None


    candles = data["result"]["list"]


    return candles



def save_candles(
    symbol,
    timeframe,
    candles
):

    path = (
        f"{OUTPUT_DIR}/"
        f"{symbol}_"
        f"{timeframe}.json"
    )


    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "updated": str(datetime.now()),
                "count": len(candles),
                "candles": candles
            },
            f,
            indent=2
        )



def run_loader():

    symbols = load_symbols()


    print("==============================")
    print("BYBIT CANDLE LOADER")
    print("==============================")

    print(
        "SYMBOLS:",
        len(symbols)
    )

    total = (
        len(symbols)
        *
        len(TIMEFRAMES)
    )

    print(
        "MARKETS:",
        total
    )

    print()


    done = 0


    for symbol in symbols:

        for tf, interval in TIMEFRAMES.items():

            try:

                candles = get_candles(
                    symbol,
                    interval
                )


                if candles:

                    save_candles(
                        symbol,
                        tf,
                        candles
                    )


                done += 1


                print(
                    f"[{done}/{total}]",
                    symbol,
                    tf
                )


                time.sleep(0.05)


            except Exception as e:

                print(
                    "ERROR",
                    symbol,
                    tf,
                    e
                )


    print()
    print("==============================")
    print("CANDLE LOADER COMPLETE")
    print("==============================")



if __name__ == "__main__":

    run_loader()
