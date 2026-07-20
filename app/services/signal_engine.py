import pandas as pd
import joblib
from datetime import datetime

MODEL="models/trading_model.pkl"
DATA="dataset/training_ready.csv"

print("START SIGNAL ENGINE...")
print()

model=joblib.load(MODEL)

df=pd.read_csv(DATA)

drop=[
    "target",
    "symbol",
    "timeframe",
    "trend"
]

X=df.drop(columns=drop)

last=X.tail(1)

proba=model.predict_proba(last)[0]
pred=model.predict(last)[0]

signals={
    0:"SELL",
    1:"HOLD",
    2:"BUY"
}

signal=signals[pred]

confidence=max(proba)*100

price=float(last["close"].values[0])

print("==============================")
print("BYBIT PRO TERMINAL X")
print("==============================")
print("TIME:",datetime.now())
print("PRICE:",price)
print()
print("SIGNAL:",signal)
print("CONFIDENCE:",round(confidence,2),"%")
print()
print("SELL:",round(proba[0]*100,2),"%")
print("HOLD:",round(proba[1]*100,2),"%")
print("BUY :",round(proba[2]*100,2),"%")
print("==============================")

if signal=="BUY" and confidence>=70:
    print("ACTION: OPEN LONG")

elif signal=="SELL" and confidence>=70:
    print("ACTION: OPEN SHORT")

else:
    print("ACTION: WAIT")

print("==============================")
