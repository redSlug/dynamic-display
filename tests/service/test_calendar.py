import datetime
from unittest.mock import patch

import pytest
import pytz

from service.calendar import (
    get_formatted_events,
    write_calendar_data,
    get_calendar_text,
)
from service.util import CALENDAR_TOKEN


@pytest.mark.skip(reason="skipping for now")
@patch("service.calendar._get_now")
@patch("service.calendar._get_raw_events")
def test_write_formatted_events(m_get_raw, m_now):
    m_now.return_value = datetime.datetime(
        2021, 4, 6, 15, 00, tzinfo=pytz.timezone("US/Eastern")
    )
    m_get_raw.return_value = [
        "BEGIN:VEVENT\r",
        "DTSTAMP:20210406T010505Z\r",
        "UID:calendar-event-14888@recurse.com\r",
        "DTSTART;TZID=America/New_York:20210407T063000\r",
        "DTEND;TZID=America/New_York:20210407T070000\r",
        "DESCRIPTION:Drop in for all or any part of it!\\n\\nhttps://www.recurse.com/c\r",
        " alendar/14888\r",
        "LOCATION:https://www.recurse.com/zoom/kitchen\r",
        "SUMMARY:Coffee Klatsch!\r",
        "URL:https://www.recurse.com/calendar/14888\r",
        "END:VEVENT\r",
    ]
    result = get_formatted_events(calendar_token=CALENDAR_TOKEN)
    assert result == "Coffee Klatsch! 06:30"


@patch("service.calendar.get_formatted_events")
def test_written_to_file(m_get_formatted):
    m_get_formatted.return_value = "Coffee Klatsch! 06:30"
    write_calendar_data()
    result = get_calendar_text()
    assert result == "Coffee Klatsch! 06:30 "
