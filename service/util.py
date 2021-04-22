from datetime import datetime


def special_logger(message):
    print(f"{datetime.datetime.now().isoformat()}: {message}")
