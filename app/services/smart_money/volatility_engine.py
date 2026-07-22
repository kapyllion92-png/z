class VolatilityEngine:

    def analyze(self, candles):

        result = {
            'atr_squeeze': False,
            'atr_expansion': False,
            'bollinger_squeeze': False,
            'squeeze_breakout': False,
            'score': 0,
            'reasons': []
        }

        if len(candles) < 30:
            return result


        highs = [float(c['high']) for c in candles]
        lows = [float(c['low']) for c in candles]
        closes = [float(c['close']) for c in candles]


        ranges = []

        for i in range(1, len(candles)):
            ranges.append(
                highs[i] - lows[i]
            )


        avg_range = sum(ranges[-20:]) / 20
        old_range = sum(ranges[-40:-20]) / 20


        if avg_range < old_range * 0.7:

            result['atr_squeeze'] = True
            result['score'] += 10
            result['reasons'].append(
                'ATR SQUEEZE'
            )


        if avg_range > old_range * 1.3:

            result['atr_expansion'] = True
            result['score'] += 10
            result['reasons'].append(
                'ATR EXPANSION'
            )


        middle = sum(closes[-20:]) / 20

        deviation = (
            sum(
                (x-middle)**2
                for x in closes[-20:]
            ) / 20
        ) ** 0.5


        bandwidth = deviation / middle


        if bandwidth < 0.01:

            result['bollinger_squeeze'] = True
            result['score'] += 10
            result['reasons'].append(
                'BOLLINGER SQUEEZE'
            )


        if result['atr_squeeze'] and result['atr_expansion']:

            result['squeeze_breakout'] = True
            result['score'] += 20
            result['reasons'].append(
                'SQUEEZE BREAKOUT'
            )


        return result
