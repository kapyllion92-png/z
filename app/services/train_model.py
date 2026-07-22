import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier


INPUT="dataset/training_ready.csv"
MODEL="models/trading_model.pkl"


print("LOAD DATA...")

df=pd.read_csv(INPUT)

print("ROWS:", len(df))


drop=[
    "target",
    "symbol",
    "timeframe",
    "trend"
]


X=df.drop(columns=drop)


# -1 SELL -> 0
#  0 HOLD -> 1
#  1 BUY  -> 2
y=df["target"].map({
    -1:0,
     0:1,
     1:2
})


print("FEATURES:")
print(X.columns.tolist())


print("TARGET:")
print(y.value_counts())


X_train,X_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("TRAIN MODEL...")


model=XGBClassifier(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="multi:softmax",
    num_class=3,
    n_jobs=-1,
    tree_method="hist"
)


model.fit(
    X_train,
    y_train
)


print("TEST MODEL...")


pred=model.predict(X_test)


acc=accuracy_score(
    y_test,
    pred
)


print("ACCURACY:",acc)


print(
    classification_report(
        y_test,
        pred,
        target_names=[
            "SELL",
            "HOLD",
            "BUY"
        ]
    )
)


os.makedirs(
    "models",
    exist_ok=True
)


joblib.dump(
    model,
    MODEL
)


print("SAVED:",MODEL)
