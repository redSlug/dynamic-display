import os
from unittest.mock import patch, MagicMock

import pytest

from service.util import DARK_SKY_API_KEY, LAT, LONG
from service.weather import DarkSkyWeather


@patch("service.weather.DarkSkyWeather.is_daytime")
@patch("service.weather.DarkSkyWeather._ask_dark_sky")
def test_weather(m_sky_response, m_is_day):
    m_sky_response.return_value = MagicMock()
    DarkSkyWeather(api_key="", lat="", long="").get_weather()


@patch("service.weather.DarkSkyWeather._now_timestamp")
def test_is_daytime(m_now):
    m_now.return_value = 1617577164.791521
    assert DarkSkyWeather(api_key="", lat="", long="").is_daytime(
        sunrise=1617532500, sunset=1617578700
    )


@pytest.mark.skip(reason="hits real darksky api")
def test_get_real_weather():
    DarkSkyWeather(api_key=DARK_SKY_API_KEY, lat=LAT, long=LONG)._ask_dark_sky()
