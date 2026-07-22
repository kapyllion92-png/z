import requests
import json
import os
from datetime import datetime


BYBIT_URL = "https://api.bybit.com/v5/market/instruments-info"


OUTPUT = "data/markets/bybit_symbols.json"


def load_bybit_symbols():

    params = {
        "category": "linear",
        "limit": 1000
    }

    r = requests.get(
        BYBIT_URL,
        params=params,
        timeout=15
    )

    data = r.json()

    if data["retCode"] != 0:
        raise Exception(data)

    symbols = []

    for item in data["result"]["list"]:

        if (
            item.get("status") == "Trading"
            and item.get("quoteCoin") == "USDT"
            and item.get("contractType") == "LinearPerpetual"
        ):

            symbols.append(
                {
                    "symbol": item["symbol"],
                    "baseCoin": item.get("baseCoin"),
                    "quoteCoin": item.get("quoteCoin"),
                    "status": item.get("status")
                }
            )


    os.makedirs(
        os.path.dirname(OUTPUT),
        exist_ok=True
    )


    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "updated": str(datetime.now()),
                "count": len(symbols),
                "symbols": symbols
            },
            f,
            indent=4,
            ensure_ascii=False
        )


    return symbols



if __name__ == "__main__":

    print("==============================")
    print("BYBIT MARKET SYMBOL LOADER")
    print("==============================")

    symbols = load_bybit_symbols()

    print()
    print("TOTAL ACTIVE USDT PERPETUAL:")
    print(len(symbols))

    print()

    print("FIRST 20 SYMBOLS:")

    for s in symbols[:20]:
        print(
            s["symbol"]
        )

    print()
    print("==============================")
    print("BYBIT SYMBOL LOADER OK")
    print("==============================")
