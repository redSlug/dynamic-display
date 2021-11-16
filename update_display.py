from dotenv import load_dotenv, find_dotenv

from service.banner_maker import BannerMaker
from service.calendar import write_calendar_data, get_calendar_text
from service.messages import get_recent_message
from service.util import special_logger
from service.weather import DarkSkyWeather

from service.util import DOTENV_PATH


if __name__ == "__main__":
    load_dotenv(find_dotenv(DOTENV_PATH))
    try:
        write_calendar_data()
        calendar = get_calendar_text()
    except Exception as e:
        special_logger(f"Could not get calendar data exception={e}")

    try:
        dsw = DarkSkyWeather()
        weather = dsw.get_weather()
    except Exception as e:
        special_logger(f"Could not get weather data exception={e}")
        raise

    message = get_recent_message()

    special_logger(f"message={message}")

    rc_banner = BannerMaker(banner_id="")
    rc_banner.replace_banner(weather=weather or ' ', calendar=calendar or ' ', message=message)

    banner = BannerMaker(banner_id="_2")
    banner.replace_banner(weather=weather)
