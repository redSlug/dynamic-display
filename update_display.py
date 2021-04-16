from dotenv import load_dotenv, find_dotenv

from service.banner_maker import BannerMaker
from service.calendar import write_calendar_data, get_calendar_text
from service.messages import get_recent_message
from service.util import special_logger
from service.weather import DarkSkyWeather


if __name__ == "__main__":
    load_dotenv(find_dotenv(filename="dotenv"))

    try:
        # NOTE(bdettmer): Write calendar data to file to persist in case endpoint goes down
        write_calendar_data()
    except Exception as e:
        special_logger(f"Could not write calendar data exception={e}")
        pass

    try:
        dsw = DarkSkyWeather()
        weather = dsw.get_weather()
    except Exception as e:
        special_logger(f"Could not get weather data exception={e}")
        raise

    message = get_recent_message()
    calendar = get_calendar_text()

    special_logger(f"message={message} calendar={calendar}")

    rc_banner = BannerMaker(banner_id="")
    rc_banner.replace_banner(weather=weather, calendar=calendar, message=message)

    banner = BannerMaker(banner_id="_2")
    banner.replace_banner(weather=weather)
