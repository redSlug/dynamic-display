from dataclasses import dataclass

import datetime
from darksky import forecast
from pytz import timezone

from service.util import DARK_SKY_API_KEY, LAT, LONG

tz = timezone("US/Eastern")


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


class DarkSkyWeather:
    def __init__(self, api_key=None, lat=None, long=None):
        self.api_key = api_key or DARK_SKY_API_KEY
        self.lat = lat or LAT
        self.long = long or LONG

    def _ask_dark_sky(self):
        return forecast(self.api_key, self.lat, self.long)

    def _now_timestamp(self):
        return datetime.datetime.now().timestamp()

    def is_daytime(self, sunrise, sunset):
        return sunrise < self._now_timestamp() < sunset

    def get_weather(self):
        response = self._ask_dark_sky()
        currently_icon = response.currently.icon.replace("-", "_")
        uv = None  # response.currently.uvIndex
        humidity = None  # int(response.currently.humidity * 100)
        low = int(response.daily.data[0].apparentTemperatureLow)
        high = int(response.daily.data[0].apparentTemperatureHigh)
        precipitation = int(response.currently.precipProbability * 100)
        current_temp = int(response.currently.apparentTemperature)

        summary = response.hourly.summary + " "
        temp = f"{low}-{high}F Now:{current_temp}"
        if humidity:
            summary += "humid:{humid}% ".format(humid=humidity)
        if uv:
            summary += "uv:{uv} ".format(uv=uv)
        if precipitation:
            summary += "precip:{}% ".format(precipitation)

        is_daytime = self.is_daytime(
            sunrise=response.daily.data[0].sunriseTime,
            sunset=response.daily.data[0].sunsetTime,
        )

        return WeatherData(
            currently_icon=currently_icon,
            summary=summary,
            temp=temp,
            precip=precipitation,
            is_daytime=is_daytime,
        )
