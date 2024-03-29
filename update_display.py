from dotenv import load_dotenv, find_dotenv

from service.banner_maker import BannerMaker
from service.calendar import write_calendar_data, get_calendar_text
from service.messages import get_recent_message
from service.util import special_logger
from service.weather import DarkSkyWeather, WeatherData

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
        weather = WeatherData(
            currently_icon="clear_day",
            summary="dark sky broke, sorry",
            temp="110.9",
            precip="0.0",
            is_daytime=True,  # TODO use time to guess
        )

    message = get_recent_message()

    special_logger(f"message={message}")

    rc_banner = BannerMaker(banner_id="")
    rc_banner.replace_banner(weather=weather, calendar=calendar or " ", message=message)
