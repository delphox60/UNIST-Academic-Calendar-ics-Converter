import re
from bs4 import BeautifulSoup

def parse_date(year, month, date):
    ymd_match = re.compile("(20[0-9]+)년[ ]*([0-9]+)월[ ]*([0-9]+)일.*").match(date)
    if ymd_match:
        return {
            "year": ymd_match.group(1),
            "month": ymd_match.group(2),
            "date": ymd_match.group(3),
        }
    md_match = re.compile("([0-9]+)월[ ]*([0-9]+)일.*").match(date)
    if md_match:
        return {
            "year": year,
            "month": md_match.group(1),
            "date": md_match.group(2),
        }
       
    d_match = re.compile("([0-9]+)일.*").match(date)
    if d_match:
        return {
            "year": year,
            "month": month,
            "date": d_match.group(1),
        }
        

academic_calendar_soup = BeautifulSoup(open("UNIST-academic-calendar-2023.html", "r").read(), "html.parser")

semestor_tag = academic_calendar_soup.find("div", attrs = {"class":"semester_cal_ro year2023"})

monthly_tags = semestor_tag.find_all("tbody")

year = 2023

for tag in monthly_tags:
    month = tag.find("th", attrs = {"class":"tac"}).text
    
    if "년" in month:
        split_text = month.split()
        year = split_text[0][:-1]
        month = split_text[1]
        
    events = tag.find_all("tr")
    
    for event in events:
        td_tags = event.find_all("td")
        if len(td_tags) == 0:
            continue
        
        date = td_tags[0].text
        event_names = list(map(lambda e : e.strip(), td_tags[1].text.strip().split('\n')))
        
        # if re.compile("([0-9]+)월.*([0-9]+)일.*\~([0-9]+)월.*([0-9]+)일.*").match(date):
        period_match = re.compile("(.*)\~(.*)").match(date)
        
        if period_match:
            start_date = parse_date(year, month, period_match.group(1).strip())
            end_date = parse_date(year, month, period_match.group(2).strip())

            continue

        date = parse_date(year, month, date)
