from bs4 import BeautifulSoup

academic_calendar_soup = BeautifulSoup(open("UNIST-academic-calendar-2023.html", "r").read(), "html.parser")