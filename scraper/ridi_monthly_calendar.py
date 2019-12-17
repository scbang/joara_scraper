import re
from urllib import parse

import requests
from bs4 import BeautifulSoup

import config
from config.ridi import make_event_url

def print_new_book_count_by_day(event_id):
    page = requests.get(make_event_url(event_id))
    page_text = page.text.replace("&#", "#")
    soup = BeautifulSoup(page_text, 'html.parser')
    event_calendar_list = soup.select(".EventCalendar")
    day_list = event_calendar_list[0].select(".EventCalendar_Publications")

    day_count_list = [0] * 31

    for day in day_list:
        day_number = int(day.select(".EventCalendar_PublicationsDayNumber")[0].text.replace(".", ""))
        day_count_list[day_number - 1] = len(day.select(".EvenetCalendar_Row"))
    sum = 0
    for day_num, day_count in enumerate(day_count_list):
        print(day_count)
        sum += day_count
    print(f"sum = {sum}")
