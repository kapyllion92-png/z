from app.services.scanner_engine import ScannerEngine

engine = ScannerEngine()

candles = []

for i in range(60):
    candles.append({
        "close": str(100 - i * 0.5),
        "volume": "5000"
    })

candles[-1]["volume"] = "50000"

result = engine.scan_symbol(
    "TESTUSDT",
    candles
)

print("RESULT:")
print(result)
