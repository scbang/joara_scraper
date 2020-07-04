import re
from urllib import parse

import requests
from bs4 import BeautifulSoup
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

import config
from data_object.author import Author


def _convert_to_int(num_string):
    if num_string is None:
        return -1;
    return int(num_string.replace(",", ""))


def _convert_to_float(num_string):
    if num_string is None:
        return -1;
    return float(num_string.replace(",", ""))


def get_free_list(date_obj):
    print("무료 순위")
    return [["무료 순위"]] + _get_list(config.FREE_QUERY, date_obj)


def get_lately_list(date_obj):
    print("신규 순위")
    return [["신규 순위"]] + _get_list(config.LATELY_QUERY, date_obj)


def _get_book_info(book_home_link, date_obj):
    first_epi_view_count = target_date_last_epi_view_count = target_date_last_epi = None
    target_date_uploaded_epi_count = 0

    url = config.HOST + book_home_link
    page = requests.get(url, cookies=config.COOKIES)
    new_location = config.HOST + page.text.split("\"")[1]

    page = requests.get(new_location, cookies=config.COOKIES)
    soup = BeautifulSoup(page.text, 'html.parser')

    css_selector = config.CSS_SELECTOR["NORMAL"]
    book_info_element_list = soup.select(css_selector["BOOK_INFO"])
    date_format = "{cur_year}/{cur_month}/{cur_day}"
    introduce_text = soup.select(".t_cont_v")[0].text.strip()
    if len(book_info_element_list) < 1:
        css_selector = config.CSS_SELECTOR["NOBLESS"]
        book_info_element_list = soup.select(css_selector["BOOK_INFO"])[1].text.split("|")
        book_total_recommend_count = book_info_element_list[1].strip().split(" ")[1]
        book_total_favorite_count = book_info_element_list[2].strip().split(" ")[1]
        date_format = "{cur_year}.{cur_month}.{cur_day}"
    else:
        book_total_recommend_count = book_info_element_list[1].text
        book_total_favorite_count = book_info_element_list[2].text

    tbl_list = soup.select(css_selector["EPISODE_DETAIL"])

    target_uploaded_date = date_format.format(**date_obj)

    for tr in tbl_list:
        chapter_cell_list = tr.select(css_selector["CELL"])
        if len(chapter_cell_list) == 6:
            episode_index = 0
            episode_date_index = 2
            episode_view_count_index = 3
        elif len(chapter_cell_list) == 8:
            episode_index = 1
            episode_date_index = 3
            episode_view_count_index = 4
        episode = chapter_cell_list[episode_index].text.replace("회", "").strip()
        episode_date = chapter_cell_list[episode_date_index].text.strip()
        first_epi_view_count = episode_view_count = chapter_cell_list[episode_view_count_index].text.strip()
        if episode_date <= target_uploaded_date:
            if not target_date_last_epi_view_count:
                target_date_last_epi = episode
                target_date_last_epi_view_count = episode_view_count
            if episode_date == target_uploaded_date:
                target_date_uploaded_epi_count += 1

    if target_date_last_epi_view_count is None:
        target_date_last_epi_view_count = "0"

    return {
        "book_total_recommend_count": _convert_to_int(book_total_recommend_count),
        "book_total_favorite_count": _convert_to_int(book_total_favorite_count),
        "first_epi_view_count": _convert_to_int(first_epi_view_count),
        "target_date_last_epi_view_count": _convert_to_int(target_date_last_epi_view_count),
        "target_date_uploaded_epi_count": target_date_uploaded_epi_count,
        "target_date_last_epi": _convert_to_int(target_date_last_epi),
        "introduce_text": introduce_text,
    }


def _get_list(query_obj, date_obj):
    query = dict(query_obj["QUERY"])
    episode_limit = query_obj["EPISODE_LIMIT"]
    headers = config.DATA_HEADERS
    book_list = [headers]
    print("|".join(headers))

    target_date = "{cur_year}{cur_month}{cur_day}".format(**date_obj)

    for page_no in query_obj["PAGE_NO_LIST"]:
        query["page_no"] = page_no
        query.update(date_obj)
        page = requests.get(config.BASE_PATH, params=query, cookies=config.COOKIES)
        page_text = page.text.replace("&#", "#")
        soup = BeautifulSoup(page_text, 'html.parser')
        tbl_list = soup.select(".tbl_list > tbody > tr")
        top_ranking = 1
        book_total_episode_count = len(tbl_list)
        for tr in tbl_list:
            td_list = tr.select("td")

            if 'class' in tr.attrs and 'top_ranking' in tr.attrs['class']:
                ranking = top_ranking
                top_ranking += 1
            else:
                ranking = int(td_list[0].text.strip())

            author_elem = td_list[1].select(".member_nickname")
            author_member_id = author_elem[0].attrs["member_id"]
            author_member_nickname = author_elem[0].text.strip()
            author = Author(author_member_id, author_member_nickname)

            title_element = td_list[2].a
            book_home_link = title_element["href"]
            genre = re.split("[\[\]]", title_element.strong.text.strip())[1]
            td_list[2].a.strong.decompose()
            titles = re.split("[<>]", title_element.text.strip())
            title = titles[0].strip()
            episode = int(titles[len(titles) - 2].strip().split("편")[0])

            if episode_limit and episode_limit < episode:
                continue

            best_score = _convert_to_int(td_list[3].text)
            favorite_count = _convert_to_int(td_list[4].text)
            recommend_count = _convert_to_int(td_list[5].text)
            view_count = _convert_to_int(td_list[6].text)

            book_code = dict(parse.parse_qsl(parse.urlsplit(book_home_link).query))["book_code"]
            book_info = _get_book_info(book_home_link, date_obj)

            book_total_recommend_count = book_info["book_total_recommend_count"]
            book_total_favorite_count = book_info["book_total_favorite_count"]
            first_epi_view_count = book_info["first_epi_view_count"]
            target_date_last_epi_view_count = book_info["target_date_last_epi_view_count"]
            target_date_uploaded_epi_count = book_info["target_date_uploaded_epi_count"]
            target_date_last_epi = book_info["target_date_last_epi"]
            introduce_text = ILLEGAL_CHARACTERS_RE.sub('', book_info["introduce_text"])

            book_total_recommend_count_num = float(book_total_recommend_count)
            book_total_favorite_count_num = float(book_total_favorite_count)
            first_epi_view_count_num = float(first_epi_view_count)
            target_date_last_epi_view_count_num = float(target_date_last_epi_view_count)

            sun_jak_bi = book_total_favorite_count_num / first_epi_view_count_num * 100.0
            yun_dok_yul = target_date_last_epi_view_count_num / first_epi_view_count_num * 100.0
            chu_choen_bi = f"{(book_total_recommend_count_num / book_total_episode_count) / book_total_favorite_count_num * 100.0:.1f}" if book_total_favorite_count_num != 0 else "N/A"

            favorite_count_per_episode = float(book_total_favorite_count) / episode
            row = {}
            i = 0
            row[headers[i]] = ranking
            i += 1
            row[headers[i]] = author.member_id
            i += 1
            row[headers[i]] = author.member_nickname
            i += 1
            row[headers[i]] = target_date
            i += 1
            row[headers[i]] = book_code
            i += 1
            row[headers[i]] = title
            i += 1
            row[headers[i]] = episode
            i += 1
            row[headers[i]] = target_date_last_epi
            i += 1
            row[headers[i]] = best_score
            i += 1
            row[headers[i]] = favorite_count
            i += 1
            row[headers[i]] = recommend_count
            i += 1
            row[headers[i]] = view_count
            i += 1
            row[headers[i]] = book_total_recommend_count
            i += 1
            row[headers[i]] = book_total_favorite_count
            i += 1
            row[headers[i]] = first_epi_view_count
            i += 1
            row[headers[i]] = target_date_last_epi_view_count
            i += 1
            row[headers[i]] = target_date_uploaded_epi_count
            i += 1
            row[headers[i]] = f"{sun_jak_bi:.1f}"
            i += 1
            row[headers[i]] = f"{yun_dok_yul:.1f}"
            i += 1
            row[headers[i]] = chu_choen_bi
            i += 1
            row[headers[i]] = f"{favorite_count_per_episode:.1f}"
            i += 1
            row[headers[i]] = f"{genre}"
            i += 1
            row[headers[i]] = f"{introduce_text}"
            print("|".join(list(map(lambda h: str(row[h]), headers))))
            book_list.append(list(map(lambda h: row[h], headers)))

    return book_list
