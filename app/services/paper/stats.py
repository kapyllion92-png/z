from pathlib import Path
import csv


BASE_DIR = Path(__file__).resolve().parents[2]

TRADES_FILE = BASE_DIR / "data" / "trades.csv"



class PaperStats:


    def report(self):


        if not TRADES_FILE.exists():

            return {
                "trades":0,
                "wins":0,
                "losses":0,
                "winrate":0,
                "profit":0
            }



        trades = 0
        wins = 0
        losses = 0
        profit = 0



        with open(
            TRADES_FILE,
            encoding="utf-8"
        ) as f:


            reader = csv.reader(f)


            for row in reader:


                if len(row) < 6:

                    continue



                trades += 1


                pnl = float(
                    row[4]
                )


                profit += pnl



                if pnl > 0:

                    wins += 1

                else:

                    losses += 1



        winrate = 0


        if trades:

            winrate = round(
                wins / trades * 100,
                2
            )



        return {

            "trades":
                trades,

            "wins":
                wins,

            "losses":
                losses,

            "winrate":
                winrate,

            "profit":
                round(
                    profit,
                    2
                )

        }
