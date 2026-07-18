def sma(values, period=14):
    if len(values) < period:
        return None

    return sum(values[-period:]) / period



def ema(values, period=14):

    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)

    ema_value = sum(values[:period]) / period

    for price in values[period:]:
        ema_value = (
            (price - ema_value) * multiplier
            + ema_value
        )

    return ema_value



def rsi(values, period=14):

    if len(values) <= period:
        return None

    gains = []
    losses = []

    for i in range(1, len(values)):
        change = values[i] - values[i - 1]

        if change > 0:
            gains.append(change)
            losses.append(0)

        else:
            gains.append(0)
            losses.append(abs(change))


    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period


    if avg_loss == 0:
        return 100


    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))



def atr(highs, lows, closes, period=14):

    if len(closes) <= period:
        return None


    true_ranges = []


    for i in range(1, len(closes)):

        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i-1]),
            abs(lows[i] - closes[i-1]),
        )

        true_ranges.append(tr)


    return sum(true_ranges[-period:]) / period
