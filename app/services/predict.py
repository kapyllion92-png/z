import pandas as pd
import joblib


MODEL = "models/trading_model.pkl"
DATA = "dataset/training_ready.csv"


print("LOAD MODEL...")
model = joblib.load(MODEL)


print("LOAD DATA...")
df = pd.read_csv(DATA)


row = df.tail(1).copy()


drop = [
    "target",
    "symbol",
    "timeframe",
    "trend"
]


X = row.drop(columns=drop)


print("FEATURES:")
print(X.columns.tolist())


prediction = model.predict(X)[0]

proba = model.predict_proba(X)[0]


classes = {
    0: "SELL",
    1: "HOLD",
    2: "BUY"
}


signal = classes[prediction]

confidence = round(float(max(proba)) * 100, 2)


print()
print("======================")
print("SIGNAL:", signal)
print("CONFIDENCE:", confidence, "%")
print("======================")
