
import time
import requests
import sqlite3


class BybitHistoryDownloader:

    BASE_URL = "https://api.bybit.com/v5/market/kline"


    def __init__(self):
        self.db = "market_history.db"


    def save_candles(self, symbol, interval, candles):

        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        for c in candles:

            cur.execute("""
            INSERT OR IGNORE INTO candles
            (
                symbol,
                interval,
                timestamp,
                open,
                high,
                low,
                close,
                volume,
                turnover
            )
            VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (
                symbol,
                interval,
                int(c[0]),
                float(c[1]),
                float(c[2]),
                float(c[3]),
                float(c[4]),
                float(c[5]),
                float(c[6])
            ))

        conn.commit()
        conn.close()


    def download(
        self,
        symbol="SOLUSDT",
        interval="15",
        target=1000000
    ):

        print("===== BYBIT HISTORY DOWNLOAD =====")
        print("COIN:",symbol)
        print("TIMEFRAME:",interval)
        print("TARGET:",target)

        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        cur.execute(
            "SELECT MIN(timestamp) FROM candles WHERE symbol=? AND interval=?",
            (symbol,interval)
        )

        row = cur.fetchone()
        conn.close()

        if not row[0]:
            end = int(time.time()*1000)
        else:
            end = row[0]


        while True:

            conn = sqlite3.connect(self.db)
            cur = conn.cursor()

            cur.execute(
                "SELECT COUNT(*) FROM candles WHERE symbol=? AND interval=?",
                (symbol,interval)
            )

            total = cur.fetchone()[0]
            conn.close()


            print("DATABASE:",total)


            if total >= target:
                break


            params = {
                "category":"linear",
                "symbol":symbol,
                "interval":interval,
                "limit":1000,
                "end":end
            }


            r = requests.get(
                self.BASE_URL,
                params=params,
                timeout=20
            )

            data = r.json()


            if "result" not in data:
                print(data)
                break


            candles = data["result"]["list"]


            if not candles:
                break


            self.save_candles(
                symbol,
                interval,
                candles
            )


            end = int(candles[-1][0])-1


            print(
                "DOWNLOADED:",
                len(candles)
            )


            time.sleep(0.2)


        print("===== DOWNLOAD COMPLETE =====")



if __name__=="__main__":

    BybitHistoryDownloader().download()
