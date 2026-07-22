from app.services.historical.history_loader import HistoryLoader
from app.services.analysis.candle_analyzer import CandleAnalyzer


loader = HistoryLoader()

db = loader.load("SOLUSDT","15")

result = CandleAnalyzer().analyze(db)

print("===== MARKET ANALYSIS =====")

for k,v in result.items():
    print(k,":",v)