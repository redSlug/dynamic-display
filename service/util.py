from datetime import datetime

DOTENV_PATH = 'env/dotenv'

def special_logger(message):
    print(f"{datetime.now().isoformat()}: {message}")
