import pandas as pd
import joblib
import requests
import time
from datetime import datetime

MODEL='models/trading_model.pkl'
SYMBOL='BTCUSDT'
INTERVAL='5'

model=joblib.load(MODEL)

features=[
'time',
'open',
'high',
'low',
'close',
'volume',
'ema20',
'ema50',
'ema200',
'rsi',
'macd',
'atr',
'momentum',
'roc',
'volume_ratio',
'vwap'
]


def get_candles():

    url='https://api.bybit.com/v5/market/kline'

    params={
        'category':'linear',
        'symbol':SYMBOL,
        'interval':INTERVAL,
        'limit':250
    }

    r=requests.get(url,params=params,timeout=10)

    data=r.json()['result']['list']

    df=pd.DataFrame(
        data,
        columns=[
            'time',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'turnover'
        ]
    )

    df=df.astype(float)

    df['ema20']=df.close.ewm(span=20).mean()
    df['ema50']=df.close.ewm(span=50).mean()
    df['ema200']=df.close.ewm(span=200).mean()

    df['rsi']=df.close.diff().rolling(14).mean()

    df['macd']=(
        df.close.ewm(span=12).mean()
        -
        df.close.ewm(span=26).mean()
    )

    df['atr']=(df.high-df.low).rolling(14).mean()

    df['momentum']=df.close.diff(10)

    df['roc']=df.close.pct_change(10)

    df['volume_ratio']=(
        df.volume /
        df.volume.rolling(20).mean()
    )

    df['vwap']=(
        df.close*df.volume
    ).cumsum()/df.volume.cumsum()

    return df.dropna()


print('START SIGNAL ENGINE...')
print()

while True:

    try:

        df=get_candles()

        X=df.tail(1)[features]

        prob=model.predict_proba(X)[0]

        pred=model.predict(X)[0]

        signals={
            0:'SELL',
            1:'HOLD',
            2:'BUY'
        }

        print('='*30)
        print('TIME:',datetime.now())
        print('PRICE:',round(float(X.close.iloc[0]),6))
        print('SIGNAL:',signals[pred])
        print('CONFIDENCE:',round(max(prob)*100,2),'%')
        print()
        print('SELL:',round(prob[0]*100,2),'%')
        print('HOLD:',round(prob[1]*100,2),'%')
        print('BUY :',round(prob[2]*100,2),'%')
        print('='*30)

    except Exception as e:
        print('ERROR:',e)

    time.sleep(60)
