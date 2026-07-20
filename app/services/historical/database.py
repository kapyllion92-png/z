import sqlite3


class HistoricalDatabase:


    def __init__(self, path="market_history.db"):

        self.connection = sqlite3.connect(path)

        self.create_tables()



    def create_tables(self):

        cursor = self.connection.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS candles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT NOT NULL,

            interval TEXT NOT NULL,

            timestamp INTEGER NOT NULL,

            open REAL,

            high REAL,

            low REAL,

            close REAL,

            volume REAL,

            turnover REAL,

            UNIQUE(symbol, interval, timestamp)

        )
        """)


        self.connection.commit()



    def save_candle(self, symbol, interval, candle):

        cursor = self.connection.cursor()


        cursor.execute("""
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
        VALUES
        (?,?,?,?,?,?,?,?,?)
        """,

        (

            symbol,

            interval,

            candle["time"],

            candle["open"],

            candle["high"],

            candle["low"],

            candle["close"],

            candle["volume"],

            candle.get("turnover",0)

        ))


        self.connection.commit()



    def get_candles(self, symbol, interval, limit=100):


        cursor = self.connection.cursor()


        cursor.execute("""
        SELECT
            timestamp,
            open,
            high,
            low,
            close,
            volume,
            turnover

        FROM candles

        WHERE symbol=? 
        AND interval=?

        ORDER BY timestamp DESC

        LIMIT ?

        """,

        (

            symbol,

            interval,

            limit

        ))


        rows = cursor.fetchall()


        candles=[]


        for r in reversed(rows):

            candles.append({

                "time": r[0],

                "open": float(r[1]),

                "high": float(r[2]),

                "low": float(r[3]),

                "close": float(r[4]),

                "volume": float(r[5]),

                "turnover": float(r[6])

            })


        return candles
