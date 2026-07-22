from typing import Dict


class DirectionEngine:


    def analyze(self, modules: Dict, score: int) -> Dict:


        result = {
            'direction': None,
            'confidence': 'NO SETUP',
            'reasons': []
        }


        structure = modules.get(
            'structure',
            {}
        )


        fvg = modules.get(
            'fvg',
            {}
        )


        order_block = modules.get(
            'order_block',
            {}
        )


        reasons_fvg = fvg.get(
            'reasons',
            []
        )


        bullish_structure = (
            structure.get('higher_high')
            and
            structure.get('higher_low')
        )


        bullish_bos = structure.get(
            'bos'
        )


        bearish_structure = (
            structure.get('lower_low')
            and
            structure.get('lower_high')
        )


        bearish_bos = structure.get(
            'bearish_bos'
        )


        bullish_confirmation = False
        bearish_confirmation = False


        if (
            fvg.get('imbalance')
            or
            'Imbalance' in reasons_fvg
            or
            order_block.get('bullish_ob')
        ):

            bullish_confirmation = True


        if (
            order_block.get('bearish_ob')
            or
            bearish_structure
        ):

            bearish_confirmation = True



        if bullish_structure and bullish_bos:

            result['reasons'].append(
                'BULLISH STRUCTURE'
            )


        if bearish_structure and bearish_bos:

            result['reasons'].append(
                'BEARISH STRUCTURE'
            )



        if bullish_structure and bullish_bos and bullish_confirmation and score >= 45:

            result['direction'] = 'LONG'


        elif bearish_structure and bearish_bos and bearish_confirmation and score >= 45:

            result['direction'] = 'SHORT'



        if score >= 70:

            result['confidence'] = 'A SETUP'

        elif score >= 55:

            result['confidence'] = 'B SETUP'

        elif score >= 45:

            result['confidence'] = 'C SETUP'


        return result
