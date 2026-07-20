from app.services.bybit_client import BybitClient


SIGNALS = []


class ScannerEngine:

    def __init__(self):

        self.client = BybitClient()

        try:
            from app.services.indicator_engine import IndicatorEngine
            self.indicator_engine = IndicatorEngine()
        except Exception:
            self.indicator_engine = None

        try:
            from app.services.strategy_engine import StrategyEngine
            self.strategy_engine = StrategyEngine()
        except Exception:
            self.strategy_engine = None

        try:
            from app.services.trade_ranker import TradeRanker
            self.ranker = TradeRanker()
        except Exception:
            self.ranker = None

        try:
            from app.services.entry_predictor import EntryPredictor
            self.ai = EntryPredictor()
        except Exception:
            self.ai = None


    def scan_symbol(self, symbol, candles):

        try:

            if len(candles) < 50:
                return None


            closes = []
            volumes = []


            for c in candles:

                if isinstance(c, list):

                    closes.append(float(c[4]))
                    volumes.append(float(c[5]))

                elif isinstance(c, dict):

                    closes.append(float(c["close"]))
                    volumes.append(float(c["volume"]))


            price = closes[-1]


            score = 0
            reasons = []


            features = {

                "symbol": symbol,
                "candles": candles,
                "price": price,
                "close": price,
                "sma": (sum(closes[-20:]) / 20),
                "high": max(closes[-20:]),
                "low": min(closes[-20:]),
                "closes": closes,
                "volumes": volumes

            }


            # =====================
            # INDICATORS
            # =====================

            gains = []
            losses = []


            for i in range(1,15):

                diff = closes[-i] - closes[-i-1]

                if diff >= 0:
                    gains.append(diff)
                else:
                    losses.append(abs(diff))


            avg_gain = sum(gains)/14 if gains else 0
            avg_loss = sum(losses)/14 if losses else 1


            rs = avg_gain / avg_loss


            rsi = round(
                100 - (100/(1+rs)),
                2
            )


            avg_volume = (
                sum(volumes[-20:])
                /
                20
            )


            volume_x = round(
                volumes[-1] / avg_volume,
                2
            )


            if rsi < 35:

                score += 10

                reasons.append(
                    "RSI перепроданность"
                )


            if volume_x > 2:

                score += 10

                reasons.append(
                    f"Volume x{volume_x}"
                )



            # =====================
            # PRICE ACTION
            # =====================

            high = max(closes[-20:])


            drop = (
                (high-price)
                /
                high
                *
                100
            )


            if drop > 5:

                score += 10

                reasons.append(
                    "Сильный откат"
                )


            # =====================
            # STRATEGIES
            # =====================

            strategy_result = None


            if self.strategy_engine:

                try:

                    strategy_result = (
                        self.strategy_engine.analyze(features)
                    )


                    if strategy_result:

                        score += 20

                        reasons.append(
                            "Strategy confirmation"
                        )


                except Exception as e:

                    print(
                        "Strategy error:",
                        e
                    )



            # =====================
            # AI
            # =====================

            ai_result = None


            if self.ai:

                try:

                    ai_result = (
                        self.ai.predict(features, strategy_result)
                    )


                    confidence = 0


                    if isinstance(ai_result, dict):

                        confidence = (
                            ai_result.get(
                                "confidence",
                                0
                            )
                        )


                    if confidence:

                        score += int(
                            confidence * 20
                        )


                        reasons.append(
                            f"AI {confidence:.0%}"
                        )


                except Exception as e:

                    print(
                        "AI error:",
                        e
                    )



            # =====================
            # FINAL RANK
            # =====================

            if self.ranker:

                try:

                    score = self.ranker.rank(
                        score,
                        features,
                        strategy_result,
                        ai_result
                    )

                except Exception:

                    pass



            score = min(
                score,
                100
            )


            if score < 50:

                return None



            # =====================
            # RISK
            # =====================

            stop = price * 0.985

            take1 = price * 1.02

            take2 = price * 1.04

            take3 = price * 1.06



            signal = {

                "symbol": symbol,

                "direction": "LONG",

                "score": score,

                "price": round(
                    price,
                    6
                ),

                "entry": round(
                    price,
                    6
                ),

                "stop": round(
                    stop,
                    6
                ),

                "take1": round(
                    take1,
                    6
                ),

                "take2": round(
                    take2,
                    6
                ),

                "take3": round(
                    take3,
                    6
                ),

                "rsi": rsi,

                "volume_x": volume_x,

                "indicators": features.get("indicators", {}),

                "reasons": reasons

            }


            print(
                "SIGNAL:",
                signal
            )


            return signal



        except Exception as e:

            print(
                "SCAN ERROR",
                symbol,
                e
            )

            return None




def get_signals():

    global SIGNALS


    SIGNALS = []


    client = BybitClient()


    symbols = client.get_symbols()


    engine = ScannerEngine()



    print(
        "Монет:",
        len(symbols)
    )


    for symbol in symbols:

        try:

            candles = client.get_candles(
                symbol
            )


            result = engine.scan_symbol(
                symbol,
                candles
            )


            if result:

                SIGNALS.append(
                    result
                )


        except Exception as e:

            print(
                symbol,
                e
            )



    SIGNALS.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return SIGNALS[:10]











