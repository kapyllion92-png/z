from typing import Dict, List


class OrderBlockEngine:


    def analyze(self, candles: List[Dict]) -> Dict:

        result = {
            'bullish_ob': False,
            'bearish_ob': False,
            'breaker_block': False,
            'mitigation': False,
            'ob_retest': False,
            'confirmation': False,
            'score': 0,
            'reasons': []
        }


        if len(candles) < 10:
            return result


        opens = [float(c.get('open',0)) for c in candles]
        highs = [float(c.get('high',0)) for c in candles]
        lows = [float(c.get('low',0)) for c in candles]
        closes = [float(c.get('close',0)) for c in candles]


        last = candles[-1]


        # ==========================
        # BULLISH ORDER BLOCK
        # ==========================

        for i in range(len(candles)-5, len(candles)-1):

            if closes[i] < opens[i]:

                if closes[-1] > highs[i]:

                    result['bullish_ob'] = True
                    result['score'] += 20
                    result['reasons'].append(
                        'BULLISH ORDER BLOCK'
                    )
                    break



        # ==========================
        # BEARISH ORDER BLOCK
        # ==========================

        for i in range(len(candles)-5, len(candles)-1):

            if closes[i] > opens[i]:

                if closes[-1] < lows[i]:

                    result['bearish_ob'] = True
                    result['score'] += 20
                    result['reasons'].append(
                        'BEARISH ORDER BLOCK'
                    )
                    break



        # ==========================
        # MITIGATION
        # ==========================

        if result['bullish_ob'] or result['bearish_ob']:

            body = abs(closes[-1]-opens[-1])

            if body > 0:

                result['mitigation'] = True
                result['score'] += 10
                result['reasons'].append(
                    'ORDER BLOCK MITIGATION'
                )



        # ==========================
        # BREAKER BLOCK
        # ==========================

        if result['bearish_ob'] and closes[-1] > highs[-2]:

            result['breaker_block'] = True
            result['score'] += 15
            result['reasons'].append(
                'BULLISH BREAKER BLOCK'
            )


        if result['bullish_ob'] and closes[-1] < lows[-2]:

            result['breaker_block'] = True
            result['score'] += 15
            result['reasons'].append(
                'BEARISH BREAKER BLOCK'
            )



        # ==========================
        # OB RETEST
        # ==========================

        if result['bullish_ob'] or result['bearish_ob']:

            result['ob_retest'] = True
            result['score'] += 10
            result['reasons'].append(
                'OB RETEST'
            )



        # ==========================
        # CONFIRMATION
        # ==========================

        if result['score'] >= 30:

            result['confirmation'] = True
            result['score'] += 5
            result['reasons'].append(
                'ORDER BLOCK CONFIRMATION'
            )


        return result
