import re
import datetime
import requests
import pytz

from service.util import special_logger, CALENDAR_TOKEN

SUMMARY_LIMIT = 25
CALENDAR_DATA_LIMIT = 120
MAX_EVENTS_SHOWN = 3
CALENDAR_DATA = "generated/calendar_data"


class Event:
    def __init__(self):
        self.start_time = None
        self.summary = None
        self.status = None


def get_line_contents(line):
    return re.search("^.*:(.*)", line).group(1)


def get_short_summary(s):
    if len(s) <= SUMMARY_LIMIT:
        return s
    result = ""

    for w in s.split():
        if len(result + w) > SUMMARY_LIMIT - 3:
            result += "..."
            break
        result += " " + w
    return result


def _get_raw_events(calendar_url):
    return requests.get(url=calendar_url).text.split("\n")


def _get_now():
    return datetime.datetime.now(pytz.timezone("US/Eastern"))


def get_formatted_events(calendar_token):
    calendar_url = "https://www.recurse.com/calendar/events.ics?token=" + calendar_token
    raw_events = _get_raw_events(calendar_url=calendar_url)
    now = _get_now()
    events = list()
    event = None
    for raw_event in raw_events:
        raw_event = raw_event.strip()
        if event and raw_event.startswith("SUMMARY"):
            event.summary = get_line_contents(raw_event)
        elif event and raw_event.startswith("STATUS"):
            event.status = get_line_contents(raw_event)
        elif event and raw_event.startswith("DTSTART"):
            start_time = get_line_contents(raw_event)
            start_time = datetime.datetime.strptime(start_time, "%Y%m%dT%H%M%S")
            event.start_time = pytz.timezone("US/Eastern").localize(start_time)
        elif raw_event.startswith("BEGIN:VEVENT"):
            event = Event()
        elif raw_event.startswith("END:VEVENT"):
            events.append(event)
            event = None

    # filter events
    events = [e for e in events if e.summary]
    events = [
        e for e in events if now < e.start_time < now + datetime.timedelta(hours=16)
    ]
    events = [e for e in events if e.status != "CANCELLED"]
    events = [e for e in events if "office hours" not in e.summary.lower()]

    # make summaries short
    for event in events:
        event.summary = get_short_summary(event.summary)

    events.sort(key=lambda x: x.start_time)

    events_string = ""
    for event in events[:MAX_EVENTS_SHOWN]:
        summary = event.summary
        time = event.start_time.strftime("%H:%M")
        if len(events_string + summary + time) + 2 > CALENDAR_DATA_LIMIT:
            break
        events_string += "{summary} {time}, ".format(summary=summary, time=time)

    return events_string[:-2]


def get_api_calendar_text():
    event_data = get_formatted_events(CALENDAR_TOKEN)
    return event_data.rstrip() + " "


def write_calendar_data():
    event_data = get_formatted_events(CALENDAR_TOKEN)
    with open(CALENDAR_DATA, "w") as f:
        f.write(event_data)


def get_calendar_text():
    try:
        with open(CALENDAR_DATA) as f:
            line = f.readline()
            return line.rstrip() + " "  # hack to avoid div by zero creating img
    except Exception:
        special_logger("unable to get calendar data")
        return " "  # hack to avoid div by zero creating img
