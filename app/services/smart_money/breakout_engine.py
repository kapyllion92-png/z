from typing import Dict, List


class BreakoutEngine:


    def analyze(self, candles: List[Dict]) -> Dict:

        result = {
            'true_breakout': False,
            'false_breakout': False,
            'retest': False,
            'range_breakout': False,
            'volume_breakout': False,
            'weak_breakout': False,
            'accumulation_breakout': False,
            'score': 0,
            'reasons': []
        }


        if len(candles) < 10:
            return result


        highs = [
            float(c.get('high',0))
            for c in candles
        ]

        lows = [
            float(c.get('low',0))
            for c in candles
        ]

        closes = [
            float(c.get('close',0))
            for c in candles
        ]

        volumes = [
            float(c.get('volume',0))
            for c in candles
        ]


        last_close = closes[-1]

        range_high = max(highs[-10:-1])
        range_low = min(lows[-10:-1])



        # ==========================
        # RANGE BREAKOUT
        # ==========================

        if last_close > range_high:

            result['range_breakout'] = True
            result['score'] += 15
            result['reasons'].append(
                'RANGE BREAKOUT'
            )


        elif last_close < range_low:

            result['range_breakout'] = True
            result['score'] += 15
            result['reasons'].append(
                'RANGE BREAKDOWN'
            )



        # ==========================
        # TRUE BREAKOUT
        # ==========================

        if result['range_breakout']:

            body = abs(
                closes[-1] - candles[-1].get('open', closes[-1])
            )

            candle_range = highs[-1] - lows[-1]


            if candle_range > 0 and body / candle_range > 0.6:

                result['true_breakout'] = True
                result['score'] += 20
                result['reasons'].append(
                    'TRUE BREAKOUT'
                )

            else:

                result['weak_breakout'] = True
                result['score'] += 5
                result['reasons'].append(
                    'WEAK BREAKOUT'
                )



        # ==========================
        # FALSE BREAKOUT
        # ==========================

        if highs[-1] > range_high and closes[-1] < range_high:

            result['false_breakout'] = True
            result['score'] += 20
            result['reasons'].append(
                'FALSE BREAKOUT'
            )


        if lows[-1] < range_low and closes[-1] > range_low:

            result['false_breakout'] = True
            result['score'] += 20
            result['reasons'].append(
                'FALSE BREAKDOWN'
            )



        # ==========================
        # RETEST
        # ==========================

        if result['true_breakout']:

            if abs(closes[-1]-range_high) / range_high < 0.02:

                result['retest'] = True
                result['score'] += 10
                result['reasons'].append(
                    'BREAKOUT RETEST'
                )



        # ==========================
        # VOLUME BREAKOUT
        # ==========================

        if len(volumes) >= 10:

            avg_volume = sum(
                volumes[-10:-1]
            ) / 9


            if avg_volume > 0 and volumes[-1] > avg_volume * 1.5:

                result['volume_breakout'] = True
                result['score'] += 15
                result['reasons'].append(
                    'HIGH VOLUME BREAKOUT'
                )



        # ==========================
        # ACCUMULATION BREAKOUT
        # ==========================

        if result['range_breakout']:

            if max(volumes[-5:]) >= max(volumes[-10:-5]):

                result['accumulation_breakout'] = True
                result['score'] += 10
                result['reasons'].append(
                    'ACCUMULATION BREAKOUT'
                )



        return result
