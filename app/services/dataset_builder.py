import os
import sys
sys.path.append(os.getcwd())
import json
import csv
from datetime import datetime

from app.services.smart_money.choch_engine import detect_choch
from app.services.smart_money.order_block_engine import order_block_engine_v17000


INPUT_DIR = "data/candles"
OUTPUT_DIR = "data/dataset"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "smart_money_dataset.csv"
)


def convert_candles(raw):

    candles = []

    for x in raw:

        candles.append(
            {
                "open": float(x[1]),
                "high": float(x[2]),
                "low": float(x[3]),
                "close": float(x[4]),
                "volume": float(x[5])
            }
        )

    return candles



def build_dataset():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    rows = []

    files = [
        f for f in os.listdir(INPUT_DIR)
        if f.endswith(".json")
    ]


    print("FILES:", len(files))


    processed = 0


    for file in files:

        path = os.path.join(
            INPUT_DIR,
            file
        )


        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)


            symbol = data.get(
                "symbol",
                "UNKNOWN"
            )

            timeframe = data.get(
                "timeframe",
                "UNKNOWN"
            )


            candles = convert_candles(
                data["candles"]
            )


            if len(candles) < 50:
                continue



            ob = order_block_engine_v17000(
                candles
            )


            blocks = ob.get(
                "top_order_blocks",
                []
            )


            choch = detect_choch(
                candles,
                order_blocks=blocks
            )


            last = candles[-1]


            rows.append(
                {

                "symbol":
                    symbol,

                "timeframe":
                    timeframe,

                "close":
                    last["close"],


                "liquidity":
                    choch.get(
                        "debug",
                        {}
                    ).get(
                        "sweep_low",
                        False
                    ),


                "order_blocks":
                    len(blocks),


                "choch":
                    choch.get(
                        "choch"
                    ),


                "bos":
                    choch.get(
                        "bos"
                    ),


                "score":
                    choch.get(
                        "score",
                        0
                    ),


                "prediction":
                    choch.get(
                        "prediction",
                        "WAIT"
                    ),


                "time":
                    datetime.now()

                }

            )


            processed += 1


            if processed % 100 == 0:

                print(
                    "PROCESSED:",
                    processed
                )


        except Exception as e:

            print(
                "ERROR:",
                file,
                e
            )



    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:


        writer = csv.DictWriter(
            f,
            fieldnames=rows[0].keys()
        )


        writer.writeheader()

        writer.writerows(
            rows
        )


    print("====================")
    print("DATASET COMPLETE")
    print("ROWS:", len(rows))
    print(
        "FILE:",
        OUTPUT_FILE
    )
    print("====================")



if __name__ == "__main__":

    build_dataset()
