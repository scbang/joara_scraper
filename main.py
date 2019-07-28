import datetime
import os
import sys

import openpyxl

import config
import scraper


def _get_excel_sheet_name():
    pass


def main(date_str, file_name):
    sheet_rows = []
    execution_datetime_str = str(datetime.datetime.now())
    line = f"조아라 투베 분석기 - 실행일시 : {execution_datetime_str}"
    sheet_rows.append([line])
    print(line)
    line = f"조회 날짜 : {date_str}"
    sheet_rows.append([line])
    print(line)

    date_obj = {
        'cur_year':  date_str[0:2],
        'cur_month': date_str[2:4],
        'cur_day':   date_str[4:6],
    }

    if os.path.isfile(file_name):
        xlsx_obj = openpyxl.load_workbook(file_name)
    else:
        xlsx_obj = openpyxl.Workbook()

    sheet = xlsx_obj.create_sheet(title=execution_datetime_str.replace(":", "-"))

    sheet_rows = sheet_rows + scraper.today_best.get_free_list(date_obj)
    sheet_rows = sheet_rows + scraper.today_best.get_lately_list(date_obj)

    for row in sheet_rows:
        sheet.append(row)
    xlsx_obj.save(file_name)


if __name__ == "__main__":
    today = datetime.date.today()
    date_string = sys.argv[1] if len(sys.argv) >= 2 else f"{today.year%100:02d}{today.month:02d}{today.day:02d}"
    file_name = sys.argv[2] if len(sys.argv) >= 3 else config.DEFAULT_RESULT_XLSX_FILE_NAME
    main(date_string, file_name)
