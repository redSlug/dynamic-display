import datetime

from dotenv import load_dotenv, find_dotenv
from pytz import timezone

from service.banner_maker import BannerMaker
from service.calendar import write_calendar_data, get_calendar_text
from service.messages import get_recent_user_message
from service.util import special_logger
from service.weather import get_weather, WeatherData

from service.util import DOTENV_PATH

tz = timezone("US/Eastern")

# update_display.py runs every 5 minutes via crontab, so this window lines up
# with the first run after each hour turns over.
TOP_OF_HOUR_MINUTE_THRESHOLD = 5


def is_top_of_hour() -> bool:
    return datetime.datetime.now(tz).minute < TOP_OF_HOUR_MINUTE_THRESHOLD


if __name__ == "__main__":
    load_dotenv(find_dotenv(DOTENV_PATH))
    calendar = " "
    try:
        write_calendar_data()
        calendar = get_calendar_text()
    except Exception as e:
        special_logger(f"Could not get calendar data exception={e}")

    try:
        recurse_weather_endpoint = (
            "https://api.weather.gov/gridpoints/OKX/34,41/forecast"
        )
        weather = get_weather(recurse_weather_endpoint)
    except Exception as e:
        special_logger(f"Could not get weather data exception={e}")
        weather = WeatherData(
            currently_icon="clear_day",
            summary="I am broken",
            temp="112F",
            precip="",
            is_daytime=True,
        )

    def is_affirming_time_of_day() -> bool:
        return weather.is_daytime

    message = get_recent_user_message()

    special_logger(f"message={message}")

    rc_banner = BannerMaker(banner_id="")
    rc_banner.replace_banner(weather=weather, calendar=calendar, message=message)

    low_power_banner = BannerMaker(banner_id="_low_power", low_power=True)
    if is_top_of_hour():
        low_power_banner.replace_banner(weather=weather, calendar=calendar, message=message)
    else:
        low_power_banner.replace_banner(weather=weather)
