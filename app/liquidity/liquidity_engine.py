import pandas as pd

def find_equal_highs(df, tolerance=0.001):
    pools=[]

    for i in range(1,len(df)):
        prev=df.high.iloc[i-1]
        curr=df.high.iloc[i]

        if abs(curr-prev)/prev <= tolerance:
            pools.append({
                "type":"EQUAL_HIGH",
                "level":float((curr+prev)/2),
                "index":i
            })

    return pools


def find_equal_lows(df, tolerance=0.001):
    pools=[]

    for i in range(1,len(df)):
        prev=df.low.iloc[i-1]
        curr=df.low.iloc[i]

        if abs(curr-prev)/prev <= tolerance:
            pools.append({
                "type":"EQUAL_LOW",
                "level":float((curr+prev)/2),
                "index":i
            })

    return pools


def detect_liquidity_sweep(df):

    result={
        "sweep":False,
        "direction":None,
        "level":None
    }

    if len(df)<3:
        return result

    last=df.iloc[-1]
    prev=df.iloc[-2]

    if last.high > prev.high and last.close < prev.high:
        result["sweep"]=True
        result["direction"]="SHORT"
        result["level"]=float(prev.high)

    elif last.low < prev.low and last.close > prev.low:
        result["sweep"]=True
        result["direction"]="LONG"
        result["level"]=float(prev.low)

    return result
