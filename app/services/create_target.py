import pandas as pd
import numpy as np

INPUT="dataset/training_dataset.csv"
OUTPUT="dataset/training_ready.csv"

print("LOAD DATA...")
df=pd.read_csv(INPUT)

print("CREATE TARGET...")

future = df.groupby(
    ["symbol","timeframe"]
)["close"].shift(-5)

change = (future - df["close"]) / df["close"] * 100

df["target"]=0

df.loc[change > 0.3,"target"]=1
df.loc[change < -0.3,"target"]=-1

df=df.dropna()

print("TARGET:")
print(df["target"].value_counts())

print("SAVE...")
df.to_csv(
    OUTPUT,
    index=False
)

print("READY:",OUTPUT)
print("ROWS:",len(df))
