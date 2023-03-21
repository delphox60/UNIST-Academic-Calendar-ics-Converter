from bs4 import BeautifulSoup

academic_calendar_soup = BeautifulSoup(open("UNIST-academic-calendar-2023.html", "r").read(), "html.parser")

semestor_tag = academic_calendar_soup.find("div", attrs = {"class":"semester_cal_ro year2023"})

monthly_tags = semestor_tag.find_all("tbody")
