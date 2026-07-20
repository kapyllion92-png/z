from app.services.indicator_engine import IndicatorEngine
from app.services.score_engine import ScoreEngine
from app.services.entry_predictor import EntryPredictor


class MarketAnalyzer:


    def __init__(self):

        self.indicators = IndicatorEngine()

        self.score = ScoreEngine()

        self.predictor = EntryPredictor()



    def analyze(self, candles):


        print(":", len(candles))


        features = self.indicators.analyze(candles)


        print("FEATURES:", features)



        result = self.score.calculate(
            features,
            [],
            0
        )



        if isinstance(result, tuple):

            score = result[0]

            reasons = result[1]

        else:

            score = result.get(
                "score",
                0
            )

            reasons = result.get(
                "reasons",
                []
            )



        rsi = features.get(
            "rsi",
            50
        )

        macd = features.get(
            "macd",
            0
        )

        trend = features.get(
            "trend",
            ""
        )

        momentum = features.get(
            "momentum",
            0
        )



        price = self.get_price(
            candles
        )


        vwap = features.get(
            "vwap",
            price
        )


        atr = features.get(
            "atr",
            price * 0.01
        )



        signal = "WAIT"



        if (

            trend == "BEARISH"

            and macd < 0

            and momentum < 0

            and price < vwap

        ):

            signal = "SHORT"


            reasons.append(
                "Bearish trend confirmation"
            )


            if rsi < 30:

                reasons.append(
                    "RSI oversold warning"
                )



        elif (

            trend == "BULLISH"

            and macd > 0

            and momentum > 0

            and price > vwap

        ):

            signal = "LONG"


            reasons.append(
                "Bullish trend confirmation"
            )



        confidence = min(
            100,
            max(
                0,
                score
            )
        )



        strategy = {

            "signal": signal,

            "score": score,

            "confidence": confidence,

            "reasons": list(
                set(reasons)
            )

        }



        prediction = self.predictor.predict(

            {

                "close": price,

                "rsi": rsi,

                "macd": macd,

                "trend": trend,

                "atr": atr

            },

            strategy

        )



        trade = {


            "status":

                prediction["status"],


            "direction":

                prediction["direction"],


            "entry_zone":

                prediction["entry_zone"],


            "stop_loss":

                prediction["stop_loss"],


            "take_profit":

                prediction["take_profit"],


            "risk_reward":

                prediction["risk_reward"],


            "confidence":

                prediction["confidence"],


            "time_window":

                prediction["time_window"]

        }



        return {


            "features":

                features,


            "strategy":

                strategy,


            "structure":{


                "trend":

                    trend,


                "rsi":

                    rsi,


                "macd":

                    macd

            },


            "ranking":

                strategy,


            "entry":

            {

                "price":

                    price

            },


            "prediction":

                prediction,


            "trade_plan":

                trade

        }




    def get_price(self,candles):


        last = candles[-1]


        if isinstance(
            last,
            dict
        ):

            return float(
                last["close"]
            )


        return float(
            last[4]
        )
