import pandas as pd
import joblib

MODEL="models/trading_model.pkl"
DATA="dataset/training_ready.csv"

print("LOAD MODEL...")
model=joblib.load(MODEL)

print("LOAD DATA...")
df=pd.read_csv(DATA)

drop=[
    "target",
    "symbol",
    "timeframe",
    "trend"
]

X=df.drop(columns=drop)

last=X.tail(1)

print("FEATURES:")
print(last.columns.tolist())

print("")
print("PREDICT...")

proba=model.predict_proba(last)[0]
pred=model.predict(last)[0]

signals={
    0:"SELL",
    1:"HOLD",
    2:"BUY"
}

signal=signals[pred]

print("======================")
print("SIGNAL:",signal)
print("CONFIDENCE:",round(max(proba)*100,2),"%")
print("======================")

print("")
print("PROBABILITIES:")
print("SELL:",round(proba[0]*100,2),"%")
print("HOLD:",round(proba[1]*100,2),"%")
print("BUY :",round(proba[2]*100,2),"%")
