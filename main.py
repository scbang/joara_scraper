import datetime
import sys

import scraper


def main(date_string):
    print(f"조아라 투베 분석기 - 실행일시 : {datetime.datetime.now()}")
    print(f"조회 날짜 : {date_string}")
    date_obj = {
        'cur_year':  date_string[0:2],
        'cur_month': date_string[2:4],
        'cur_day':   date_string[4:6],
    }

    scraper.today_best.get_free_list(date_obj)
    scraper.today_best.get_lately_list(date_obj)


if __name__ == "__main__":
    today = datetime.date.today()
    date_string = sys.argv[1] if len(sys.argv) >= 2 else f"{today.year%100:02d}{today.month:02d}{today.day:02d}"
    main(date_string)
