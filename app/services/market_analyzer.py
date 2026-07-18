from app.services.features.builder import FeatureBuilder
from app.services.strategies.trend import TrendStrategy
from app.services.ranking.scorer import SignalScorer
from app.services.smart_money.structure import StructureAnalyzer
from app.services.smart_money.entry import EntryEngine



class MarketAnalyzer:


    def __init__(self):

        self.feature_builder = FeatureBuilder()

        self.trend_strategy = TrendStrategy()

        self.signal_scorer = SignalScorer()

        self.structure_analyzer = StructureAnalyzer()

        self.entry_engine = EntryEngine()



    def analyze(
        self,
        candles
    ):


        features = self.feature_builder.build(
            candles
        )


        strategy = self.trend_strategy.analyze(
            features
        )


        ranking = self.signal_scorer.score(
            features,
            strategy
        )


        structure = self.structure_analyzer.analyze(
            candles
        )


        entry = self.entry_engine.analyze(
            features,
            strategy,
            structure
        )


        return {

            "features":
                features,

            "strategy":
                strategy,

            "ranking":
                ranking,

            "structure":
                structure,

            "entry":
                entry,

        }
