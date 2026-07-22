from typing import Dict, List


class ReversalEngine:


    def analyze(self, candles: List[Dict]) -> Dict:

        result = {
            'after_pump': False,
            'after_dump': False,
            'liquidity_reversal': False,
            'level_reversal': False,
            'v_reversal': False,
            'double_top': False,
            'double_bottom': False,
            'head_shoulders': False,
            'confirmation': False,
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



        last = closes[-1]

        prev = closes[-2]



        # ==========================
        # AFTER PUMP
        # ==========================

        pump_move = (
            closes[-1] - closes[-10]
        ) / closes[-10]


        if pump_move > 0.08:

            result['after_pump'] = True
            result['score'] += 10
            result['reasons'].append(
                'AFTER PUMP'
            )



        # ==========================
        # AFTER DUMP
        # ==========================

        dump_move = (
            closes[-1] - closes[-10]
        ) / closes[-10]


        if dump_move < -0.08:

            result['after_dump'] = True
            result['score'] += 10
            result['reasons'].append(
                'AFTER DUMP'
            )



        # ==========================
        # LIQUIDITY REVERSAL
        # ==========================

        if highs[-1] > max(highs[-10:-1]) and closes[-1] < max(highs[-10:-1]):

            result['liquidity_reversal'] = True
            result['score'] += 15
            result['reasons'].append(
                'LIQUIDITY REVERSAL'
            )


        if lows[-1] < min(lows[-10:-1]) and closes[-1] > min(lows[-10:-1]):

            result['liquidity_reversal'] = True
            result['score'] += 15
            result['reasons'].append(
                'LIQUIDITY REVERSAL'
            )



        # ==========================
        # LEVEL REVERSAL
        # ==========================

        support = min(lows[-10:-1])
        resistance = max(highs[-10:-1])


        if abs(last-support)/support < 0.01:

            result['level_reversal'] = True
            result['score'] += 10
            result['reasons'].append(
                'SUPPORT REVERSAL'
            )


        if abs(last-resistance)/resistance < 0.01:

            result['level_reversal'] = True
            result['score'] += 10
            result['reasons'].append(
                'RESISTANCE REVERSAL'
            )



        # ==========================
        # V REVERSAL
        # ==========================

        if closes[-3] > closes[-2] < closes[-1]:

            result['v_reversal'] = True
            result['score'] += 10
            result['reasons'].append(
                'V REVERSAL'
            )



        # ==========================
        # DOUBLE TOP
        # ==========================

        if abs(highs[-3]-highs[-1]) / highs[-1] < 0.01:

            result['double_top'] = True
            result['score'] += 10
            result['reasons'].append(
                'DOUBLE TOP'
            )



        # ==========================
        # DOUBLE BOTTOM
        # ==========================

        if abs(lows[-3]-lows[-1]) / lows[-1] < 0.01:

            result['double_bottom'] = True
            result['score'] += 10
            result['reasons'].append(
                'DOUBLE BOTTOM'
            )



        # ==========================
        # HEAD SHOULDERS
        # ==========================

        if len(highs)>=5:

            if highs[-5] < highs[-3] and highs[-1] < highs[-3]:

                result['head_shoulders'] = True
                result['score'] += 15
                result['reasons'].append(
                    'HEAD SHOULDERS'
                )



        # ==========================
        # CONFIRMATION
        # ==========================

        if result['score'] >= 20:

            result['confirmation'] = True
            result['score'] += 10
            result['reasons'].append(
                'REVERSAL CONFIRMATION'
            )


        return result
