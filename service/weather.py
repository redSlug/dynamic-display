from dataclasses import dataclass
import requests

weather_files = dict(
    clear_day="dark_sun.ppm",
    clear_night="clear_night.ppm",
    rain="rainy.ppm",
    snow="snowflake.ppm",
    sleet="rainy.ppm",
    wind="wind1.ppm",
    fog="cloud.ppm",
    cloudy="cloud.ppm",
    partly_cloudy_day="partly_cloudy_day.ppm",
    partly_cloudy_night="partly_cloudy_night.ppm",
)


@dataclass
class WeatherData:
    currently_icon: str
    summary: str
    temp: str
    precip: int
    is_daytime: bool


def get_weather(govt_endpoint):
    headers = {"user-agent": "dynamic-display.xyz"}
    r = requests.get(govt_endpoint, headers=headers)
    data = r.json()
    period = data["properties"]["periods"][0]
    is_daytime = period.get("isDaytime", False)

    # TODO handle all icons from https://api.weather.gov/icons
    # icon field must be parsed, "icon": "https://api.weather.gov/icons/land/night/sct?size=medium"
    currently_icon = "clear_day" if is_daytime else "clear_night"
    icon = period["icon"]
    if "snow" in icon:
        currently_icon = "snow"
    elif "rain" in icon:
        currently_icon = "rain"
    elif "cloud" in icon:
        currently_icon = "cloudy"
    elif "sct" in icon or "few" in icon or "ovc" in icon:
        currently_icon = "partly_cloudy_day" if is_daytime else "partly_cloudy_night"

    return WeatherData(
        currently_icon=currently_icon,
        summary=period["shortForecast"],
        temp=f"{period['temperature']}F",
        precip=period.get("shortForecast", 0),
        is_daytime=is_daytime,
    )
