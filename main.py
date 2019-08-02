import datetime
import os
import sys

import openpyxl
from openpyxl.cell.cell import Cell
from openpyxl.styles import Font, NamedStyle, PatternFill
from openpyxl.styles.colors import BLUE, RED

import config
import scraper


def styled_cells(data, ws, style):
    for c in data:
        c = Cell(ws, value=c)
        c.style = style
        yield c


def main(date_str, file_name):
    sheet_rows = []
    execution_datetime_str = str(datetime.datetime.now())[0:19]
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

    sheet = xlsx_obj.create_sheet(title=f'{date_str} {execution_datetime_str.replace(":", "-")}')

    sheet_rows = sheet_rows + scraper.today_best.get_free_list(date_obj)
    sheet_rows = sheet_rows + scraper.today_best.get_lately_list(date_obj)

    if "over_10k_style" not in xlsx_obj.style_names:
        over_10k_favorite_color = BLUE
        over_10k_favorite_bg_color = "F0E8DD"

        over_10k_style = NamedStyle(name="over_10k_style")
        over_10k_style.font = Font(color=over_10k_favorite_color)
        over_10k_style.fill = PatternFill(start_color=over_10k_favorite_bg_color,
                                          end_color=over_10k_favorite_bg_color,
                                          fill_type="solid")

        xlsx_obj.add_named_style(over_10k_style)
    if "over_20k_style" not in xlsx_obj.style_names:
        over_20k_favorite_color = RED
        over_20k_favorite_bg_color = "D1F5EC"

        over_20k_style = NamedStyle(name="over_20k_style")
        over_20k_style.font = Font(color=over_20k_favorite_color)
        over_20k_style.fill = PatternFill(start_color=over_20k_favorite_bg_color,
                                          end_color=over_20k_favorite_bg_color,
                                          fill_type="solid")

        xlsx_obj.add_named_style(over_20k_style)

    for row in sheet_rows:
        row_style = None
        if len(row) > 13:
            try:
                book_total_favorite_count = int(row[12].replace(",", ""))
                if book_total_favorite_count >= 20000:
                    row_style = "over_20k_style"
                elif book_total_favorite_count >= 10000:
                    row_style = "over_10k_style"

                if row_style is not None:
                    row = styled_cells(row, sheet, row_style)
            except:
                pass
        sheet.append(row)

    xlsx_obj.save(file_name)


if __name__ == "__main__":
    today = datetime.date.today()
    date_string = sys.argv[1] if len(sys.argv) >= 2 else f"{today.year%100:02d}{today.month:02d}{today.day:02d}"
    file_name = sys.argv[2] if len(sys.argv) >= 3 else config.DEFAULT_RESULT_XLSX_FILE_NAME
    main(date_string, file_name)
