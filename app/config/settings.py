import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]


load_dotenv(
    BASE_DIR / ".env"
)


TRADING_MODE = os.getenv(
    "TRADING_MODE",
    "SIMULATION"
)


EXCHANGE = os.getenv(
    "EXCHANGE",
    "BYBIT"
)
