from service.banner_maker import BannerMaker
from service.weather import WeatherData


def test_banner_maker():
    weather_data = WeatherData(
        currently_icon="cloudy",
        summary="Clear throughout the day. ",
        temp="39-58F Now:50",
        precip=0,
        is_daytime=True,
    )
    BannerMaker(banner_id=1).replace_banner(
        weather=weather_data,
        calendar_text="Glaciology Seminar 12:00 ",
        message_text=" Let's hack! You can submit a PR dynamicdisplay.recurse.com ",
        train_text="",
    )
