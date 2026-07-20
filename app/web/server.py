from flask import Flask, render_template
from app.services.scanner_engine import ScannerEngine


app = Flask(
    __name__,
    template_folder="templates"
)


scanner = ScannerEngine()


@app.route("/")
def index():

    signals = []

    try:

        candles = []


        for i in range(60):

            candles.append(
                {
                    "close": str(100 - i * 0.5),
                    "volume": "5000"
                }
            )


        candles[-1]["volume"] = "50000"


        result = scanner.scan_symbol(
            "TESTUSDT",
            candles
        )


        if result:
            signals.append(result)


    except Exception as e:

        print(
            "WEB ERROR:",
            e
        )


    return render_template(
        "index.html",
        signals=signals
    )



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
