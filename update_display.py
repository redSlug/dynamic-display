from dotenv import load_dotenv, find_dotenv

from service.banner_maker import BannerMaker
from service.messages import get_recent_message
from service.util import special_logger
from service.weather import DarkSkyWeather


if __name__ == "__main__":
    load_dotenv(find_dotenv(filename="dotenv"))

    try:
        dsw = DarkSkyWeather()
        weather = dsw.get_weather()
    except Exception as e:
        special_logger(f"Could not get weather data exception={e}")
        raise

    message = get_recent_message()

    special_logger(f"message={message}")

    rc_banner = BannerMaker(banner_id="")
    rc_banner.replace_banner(weather=weather, calendar=' ', message=message)

    banner = BannerMaker(banner_id="_2")
    banner.replace_banner(weather=weather)
