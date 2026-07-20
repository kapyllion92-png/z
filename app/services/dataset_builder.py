import os
import pandas as pd
import numpy as np


DATA_DIR = "data"
OUT_DIR = "dataset"

TIMEFRAMES = [
    "5",
    "15",
    "60",
    "240",
    "D"
]


def ema(series, period):
    return series.ewm(
        span=period,
        adjust=False
    ).mean()


def rsi(series, period=14):

    delta = series.diff()

    gain = delta.where(delta > 0,0)
    loss = -delta.where(delta < 0,0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100/(1+rs))


def macd(series):

    return (
        ema(series,12)
        -
        ema(series,26)
    )


def atr(df,period=14):

    tr1=df.high-df.low

    tr2=(df.high-df.close.shift()).abs()

    tr3=(df.low-df.close.shift()).abs()

    tr=pd.concat(
        [tr1,tr2,tr3],
        axis=1
    ).max(axis=1)

    return tr.rolling(period).mean()



def make_features(df):

    df=df.copy()

    df["ema20"]=ema(df.close,20)
    df["ema50"]=ema(df.close,50)
    df["ema200"]=ema(df.close,200)

    df["rsi"]=rsi(df.close)

    df["macd"]=macd(df.close)

    df["atr"]=atr(df)

    df["momentum"]=(
        df.close -
        df.close.shift(10)
    )

    df["roc"]=(
        df.close.pct_change(10)*100
    )


    df["volume_ratio"]=(
        df.volume /
        df.volume.rolling(20).mean()
    )


    df["vwap"]=(
        (df.close*df.volume)
        .rolling(50)
        .sum()
        /
        df.volume.rolling(50).sum()
    )


    df["trend"]="NEUTRAL"

    df.loc[
        df.close>df.ema200,
        "trend"
    ]="BULLISH"


    df.loc[
        df.close<df.ema200,
        "trend"
    ]="BEARISH"


    return df



def main():

    os.makedirs(
        OUT_DIR,
        exist_ok=True
    )


    result=[]


    symbols=os.listdir(DATA_DIR)


    print(
        "TOTAL SYMBOLS:",
        len(symbols)
    )


    for symbol in symbols:


        folder=os.path.join(
            DATA_DIR,
            symbol
        )


        if not os.path.isdir(folder):
            continue


        print(
            "LOAD:",
            symbol
        )


        for tf in TIMEFRAMES:


            file=os.path.join(
                folder,
                tf+".csv"
            )


            if not os.path.exists(file):
                continue


            try:

                df=pd.read_csv(file)


                if len(df)<100:
                    continue


                df=make_features(df)


                df["symbol"]=symbol
                df["timeframe"]=tf


                result.append(df)


                print(
                    tf,
                    len(df)
                )


            except Exception as e:

                print(
                    "ERROR",
                    symbol,
                    tf,
                    e
                )


    if not result:

        print(
            "NO DATA"
        )
        return


    dataset=pd.concat(
        result,
        ignore_index=True
    )


    dataset.replace(
        [np.inf,-np.inf],
        np.nan,
        inplace=True
    )


    dataset.dropna(
        inplace=True
    )


    os.makedirs(
        OUT_DIR,
        exist_ok=True
    )


    path=os.path.join(
        OUT_DIR,
        "training_dataset.csv"
    )


    dataset.to_csv(
        path,
        index=False
    )


    print("====================")
    print("DATASET CREATED")
    print(
        "ROWS:",
        len(dataset)
    )
    print(
        "FILE:",
        path
    )



if __name__=="__main__":
    main()