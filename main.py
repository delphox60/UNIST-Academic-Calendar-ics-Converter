import re
from bs4 import BeautifulSoup

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
        event_name = td_tags[1].text
