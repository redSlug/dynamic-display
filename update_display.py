from dotenv import load_dotenv, find_dotenv

from service.banner_maker import BannerMaker
from service.calendar import write_calendar_data, get_calendar_text
from service.messages import get_recent_message
from service.util import special_logger
from service.weather import get_weather, WeatherData

from service.util import DOTENV_PATH


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
            "https://api.weather.gov/gridpoints/OKX/34,34/forecast"
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

    message = get_recent_message(
        True
    )  # TODO: maybe later update to weather.currently_icon == "clear_day"

    special_logger(f"message={message}")

    rc_banner = BannerMaker(banner_id="")
    rc_banner.replace_banner(weather=weather, calendar=calendar, message=message)
