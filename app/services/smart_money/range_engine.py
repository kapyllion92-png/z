from typing import Dict, List


class RangeEngine:


    def analyze(self, candles: List[Dict]) -> Dict:


        result = {
            'accumulation': False,
            'consolidation': False,
            'range_breakout': False,
            'false_breakout': False,
            'return_to_range': False,
            'score': 0,
            'reasons': []
        }


        if len(candles) < 20:
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



        high_range = max(highs[-20:])
        low_range = min(lows[-20:])

        range_size = (
            high_range - low_range
        ) / low_range



        # ==========================
        # CONSOLIDATION
        # ==========================

        if range_size < 0.05:

            result['consolidation'] = True
            result['score'] += 10
            result['reasons'].append(
                'CONSOLIDATION'
            )



        # ==========================
        # ACCUMULATION
        # ==========================

        avg_volume = (
            sum(volumes[-20:]) / 20
        )


        if result['consolidation'] and volumes[-1] <= avg_volume:

            result['accumulation'] = True
            result['score'] += 10
            result['reasons'].append(
                'ACCUMULATION RANGE'
            )



        # ==========================
        # RANGE BREAKOUT
        # ==========================

        if closes[-1] > high_range:

            result['range_breakout'] = True
            result['score'] += 20
            result['reasons'].append(
                'RANGE BREAKOUT'
            )


        if closes[-1] < low_range:

            result['range_breakout'] = True
            result['score'] += 20
            result['reasons'].append(
                'RANGE BREAKDOWN'
            )



        # ==========================
        # FALSE BREAKOUT
        # ==========================

        if highs[-1] > high_range and closes[-1] < high_range:

            result['false_breakout'] = True
            result['score'] += 20
            result['reasons'].append(
                'FALSE BREAKOUT'
            )


        if lows[-1] < low_range and closes[-1] > low_range:

            result['false_breakout'] = True
            result['score'] += 20
            result['reasons'].append(
                'FALSE BREAKDOWN'
            )



        # ==========================
        # RETURN TO RANGE
        # ==========================

        if result['false_breakout']:

            result['return_to_range'] = True
            result['score'] += 10
            result['reasons'].append(
                'RETURN TO RANGE'
            )



        return result
