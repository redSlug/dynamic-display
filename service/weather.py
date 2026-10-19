import datetime
import re
from dataclasses import dataclass

import requests
from pytz import timezone

tz = timezone("US/Eastern")
_DURATION_RE = re.compile(r"PT(\d+)H")

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
        precip=period["probabilityOfPrecipitation"].get("value", 0),
        is_daytime=is_daytime,
    )


def _current_hourly_period(periods, now):
    for period in periods:
        start = datetime.datetime.fromisoformat(period["startTime"])
        end = datetime.datetime.fromisoformat(period["endTime"])
        if start <= now < end:
            return period
    return periods[0]


def _current_bucketed_value(values, now):
    for value in values:
        start_str, duration_str = value["validTime"].split("/")
        start = datetime.datetime.fromisoformat(start_str)
        hours = int(_DURATION_RE.fullmatch(duration_str).group(1))
        end = start + datetime.timedelta(hours=hours)
        if start <= now < end:
            return value["value"]
    return None


def _current_apparent_temp_f(values, now):
    celsius = _current_bucketed_value(values, now)
    return celsius * 9 / 5 + 32 if celsius is not None else None


def get_hourly_weather(gridpoint_endpoint):
    headers = {"user-agent": "dynamic-display.xyz"}
    now = datetime.datetime.now(tz) + datetime.timedelta(minutes=30)

    hourly = requests.get(
        f"{gridpoint_endpoint}/forecast/hourly", headers=headers
    ).json()
    periods = hourly["properties"]["periods"]
    period = _current_hourly_period(periods, now)
    is_daytime = period.get("isDaytime", False)

    raw = requests.get(gridpoint_endpoint, headers=headers).json()
    apparent_values = raw["properties"]["apparentTemperature"]["values"]
    feels_like_f = _current_apparent_temp_f(apparent_values, now)
    temp_f = feels_like_f if feels_like_f is not None else period["temperature"]

    precip_percent = period["probabilityOfPrecipitation"].get("value", 0)
    summary = period["shortForecast"]
    if precip_percent and precip_percent > 80:
        precip_values = raw["properties"]["quantitativePrecipitation"]["values"]
        precip_mm = _current_bucketed_value(precip_values, now)
        if precip_mm is not None:
            summary = f"{summary} - {round(precip_mm)}mm"

    # TODO handle all icons from https://api.weather.gov/icons
    # icon field must be parsed, "icon": "https://api.weather.gov/icons/land/night/sct?size=medium"
    currently_icon = "clear_day" if is_daytime else "clear_night"
    icon = period["icon"]
    if "wind" in icon:
        currently_icon = "wind"
    elif "snow" in icon:
        currently_icon = "snow"
    elif "rain" in icon:
        currently_icon = "rain"
    elif "cloud" in icon:
        currently_icon = "cloudy"
    elif "sct" in icon or "few" in icon or "ovc" in icon:
        currently_icon = "partly_cloudy_day" if is_daytime else "partly_cloudy_night"

    return WeatherData(
        currently_icon=currently_icon,
        summary=summary,
        temp=f"{round(temp_f)}F",
        precip=precip_percent,
        is_daytime=is_daytime,
    )
