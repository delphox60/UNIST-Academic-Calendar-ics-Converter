import re
from pathlib import Path
import os
import datetime
import pytz
from bs4 import BeautifulSoup
from icalendar import Calendar, Event, vCalAddress, vText


def parse_date(year, month, date):
    ymd_match = re.compile("(20[0-9]+)년[ ]*([0-9]+)월[ ]*([0-9]+)일.*").match(date)
    if ymd_match:
        return datetime.date(
            int(ymd_match.group(1)), int(ymd_match.group(2)), int(ymd_match.group(3))
        )

    md_match = re.compile("([0-9]+)월[ ]*([0-9]+)일.*").match(date)
    if md_match:
        return datetime.date(int(year), int(md_match.group(1)), int(md_match.group(2)))

    d_match = re.compile("([0-9]+)일.*").match(date)
    if d_match:
        return datetime.date(int(year), int(month), int(d_match.group(1)))

calendar = Calendar()

academic_calendar_soup = BeautifulSoup(
    open("UNIST-academic-calendar-2023.html", "r").read(), "html.parser"
)

semestor_tag = academic_calendar_soup.find(
    "div", attrs={"class": "semester_cal_ro year2023"}
)

monthly_tags = semestor_tag.find_all("tbody")

year = 2023

for tag in monthly_tags:
    month = tag.find("th", attrs={"class": "tac"}).text

    if "년" in month:
        split_text = month.split()
        year = split_text[0][:-1]
        month = split_text[1]

    events = tag.find_all("tr")

    for event in events:
        td_tags = event.find_all("td")
        if len(td_tags) == 0:
            continue

        date_info = td_tags[0].text
        events = list(map(lambda e: e.strip(), td_tags[1].text.strip().split("\n")))

        period_match = re.compile("(.*)\~(.*)").match(date_info)

        if period_match:
            start_date = parse_date(year, month, period_match.group(1).strip())
            end_date = parse_date(year, month, period_match.group(2).strip())
        else:
            start_date = parse_date(year, month, date_info)
            end_date = None

        event_info = {
            "events": events,
            "start_date": start_date,
            "end_date": end_date,
        }

        for event_name in event_info["events"]:
            ic_event = Event()
            print(event_name)
            ic_event.add("summary", event_name)
            ic_event.add("dtstart", event_info["start_date"])
            if event_info["end_date"]:
                ic_event.add("dtend", event_info["end_date"])

            ic_event["dtstart"].params["VALUE"] = "DATE"
            if event_info["end_date"]:
                ic_event["dtend"].params["VALUE"] = "DATE"

            calendar.add_component(ic_event)

f = open("UNIST_academic_calendar_2023.ics", "wb")
f.write(calendar.to_ical())
f.close()
