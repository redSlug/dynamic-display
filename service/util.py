from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv


DOTENV_PATH = "/app/env/dotenv"

load_dotenv(find_dotenv(DOTENV_PATH))
DARK_SKY_API_KEY = os.getenv("DARK_SKY_API_KEY")
LAT = os.getenv("LAT")
LONG = os.getenv("LONG")
DB_URL = os.getenv("DB_URL")
CALENDAR_TOKEN = os.getenv("CALENDAR_TOKEN")


def special_logger(message):
    print(f"{datetime.now().isoformat()}: {message}")
