class PivotDetector:

    def find_pivots(self, candles, left=2, right=2):

        pivot_highs = []
        pivot_lows = []

        for i in range(left, len(candles) - right):

            high = candles[i][5]
            low = candles[i][6]

            is_high = True
            is_low = True

            for j in range(i - left, i):

                if candles[j][5] >= high:
                    is_high = False

                if candles[j][6] <= low:
                    is_low = False


            for j in range(i + 1, i + right + 1):

                if candles[j][5] > high:
                    is_high = False

                if candles[j][6] < low:
                    is_low = False


            if is_high and not is_low:

                pivot_highs.append({
                    "index": i,
                    "price": high,
                    "time": candles[i][3],
                })


            elif is_low and not is_high:

                pivot_lows.append({
                    "index": i,
                    "price": low,
                    "time": candles[i][3],
                })


        return pivot_highs, pivot_lows
