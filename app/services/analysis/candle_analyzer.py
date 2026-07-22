import statistics


class CandleAnalyzer:

    def analyze(self, candles):

        if not candles:
            return {
                "error": "no candles"
            }

        closes = [float(c[4]) for c in candles]
        volumes = [float(c[5]) for c in candles]

        first = closes[0]
        last = closes[-1]

        change = ((last - first) / first) * 100

        volatility = statistics.stdev(closes)

        avg_volume = sum(volumes) / len(volumes)

        high = max(closes)
        low = min(closes)

        return {
            "candles": len(candles),
            "first_close": first,
            "last_close": last,
            "change_percent": round(change, 3),
            "volatility": round(volatility, 5),
            "average_volume": round(avg_volume, 3),
            "range_percent": round(((high-low)/low)*100,3)
        }
