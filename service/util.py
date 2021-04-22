from datetime import datetime


def special_logger(message):
    print(f"{datetime.now().isoformat()}: {message}")
