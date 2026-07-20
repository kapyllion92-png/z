import pandas as pd

def detect_swings(df, left=3, right=3):
    highs = []
    lows = []

    for i in range(left, len(df)-right):
        high = df.high.iloc[i]
        low = df.low.iloc[i]

        left_high = df.high.iloc[i-left:i].max()
        right_high = df.high.iloc[i+1:i+right+1].max()

        left_low = df.low.iloc[i-left:i].min()
        right_low = df.low.iloc[i+1:i+right+1].min()

        if high > left_high and high > right_high:
            highs.append({
                "index": i,
                "type": "HIGH",
                "price": float(high)
            })

        if low < left_low and low < right_low:
            lows.append({
                "index": i,
                "type": "LOW",
                "price": float(low)
            })

    return {
        "highs": highs,
        "lows": lows
    }


def market_structure(df):
    swings = detect_swings(df)

    highs = swings["highs"]
    lows = swings["lows"]

    result = {
        "trend": "UNKNOWN",
        "BOS": False,
        "CHoCH": False
    }

    if len(highs) >= 2 and len(lows) >= 2:

        if highs[-1]["price"] > highs[-2]["price"]:
            result["trend"] = "BULLISH"
            result["BOS"] = True

        elif lows[-1]["price"] < lows[-2]["price"]:
            result["trend"] = "BEARISH"
            result["BOS"] = True

    return result
