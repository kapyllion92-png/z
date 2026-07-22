import os
import pandas as pd


class DataStorage:


    def __init__(self, path="data"):

        self.path = path

        os.makedirs(
            self.path,
            exist_ok=True
        )


    def save_candles(
        self,
        symbol,
        interval,
        candles
    ):

        folder=os.path.join(
            self.path,
            symbol
        )


        os.makedirs(
            folder,
            exist_ok=True
        )


        file=os.path.join(
            folder,
            f"{interval}.csv"
        )


        df=pd.DataFrame(candles)


        if os.path.exists(file):

            old=pd.read_csv(file)

            df=pd.concat(
                [
                    old,
                    df
                ]
            )


        df.drop_duplicates(
            subset=["time"],
            inplace=True
        )


        df.sort_values(
            "time",
            inplace=True
        )


        df.to_csv(
            file,
            index=False
        )



    def load_candles(
        self,
        symbol,
        interval
    ):

        file=os.path.join(
            self.path,
            symbol,
            f"{interval}.csv"
        )


        if not os.path.exists(file):

            return []


        df=pd.read_csv(file)


        return df.to_dict(
            "records"
        )
