import re

import requests
from bs4 import BeautifulSoup

import config
from data_object.author import Author


def get_free_list(date_obj):
    print("무료 순위")
    _get_list(config.FREE_QUERY, date_obj)


def get_lately_list(date_obj):
    print("신규 순위")
    _get_list(config.LATELY_QUERY, date_obj)


def _get_book_info(book_home_link, date_obj):
    first_epi_view_count = target_date_last_epi_view_count = None
    target_date_uploaded_epi_count = 0

    url = config.HOST + book_home_link
    page = requests.get(url, cookies=config.COOKIES)
    new_location = config.HOST + page.text.split("\"")[1]

    page = requests.get(new_location, cookies=config.COOKIES)
    soup = BeautifulSoup(page.text, 'html.parser')

    book_total_recommend_count = soup.select(".txt_c_sty01 > .info_c > .info2 > .date")[1].text
    tbl_list = soup.select(".tbl_work > tbody > tr")

    target_uploaded_date = f"{date_obj['cur_year']}/{date_obj['cur_month']}/{date_obj['cur_day']}"

    for tr in tbl_list:
        chapter_cell_list = tr.select("td.chapter_cell")
        episode_date = chapter_cell_list[2].text.strip()
        first_epi_view_count = episode_view_count = chapter_cell_list[3].text.strip()
        if episode_date <= target_uploaded_date:
            if not target_date_last_epi_view_count:
                target_date_last_epi_view_count = episode_view_count
            if episode_date == target_uploaded_date:
                target_date_uploaded_epi_count += 1

    return book_total_recommend_count, first_epi_view_count, target_date_last_epi_view_count, target_date_uploaded_epi_count


def _get_list(query_obj, date_obj):
    query = dict(query_obj["QUERY"])
    episode_limit = query_obj["EPISODE_LIMIT"]
    print("랭킹|작가 ID|작가 닉네임|장르|제목|최근연재회차|투데이 베스트지수|투데이 선작|투데이 추천|투데이 조회|작품 전체 추천수|첫회 조회수|수집 날짜 조회수|수집 날짜 연재 회차수")
    for page_no in query_obj["PAGE_NO_LIST"]:
        query["page_no"] = page_no
        query.update(date_obj)
        page = requests.get(config.BASE_PATH, params=query, cookies=config.COOKIES)
        soup = BeautifulSoup(page.text, 'html.parser')
        tbl_list = soup.select(".tbl_list > tbody > tr")
        top_ranking = 1
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
            episode = int(titles[1].strip().split("편")[0])

            if episode_limit and episode_limit < episode:
                continue

            best_score = td_list[3].text
            favorite_count = td_list[4].text
            recommend_count = td_list[5].text
            view_count = td_list[6].text

            book_total_recommend_count, first_epi_view_count, target_date_last_epi_view_count, target_date_uploaded_epi_count = \
                _get_book_info(book_home_link, date_obj)

            print(
                f"{ranking}"
                f"|{author}"
                f"|{genre}"
                f"|{title}"
                f"|{episode}"
                f"|{best_score}"
                f"|{favorite_count}"
                f"|{recommend_count}"
                f"|{view_count}"
                f"|{book_total_recommend_count}"
                f"|{first_epi_view_count}"
                f"|{target_date_last_epi_view_count}"
                f"|{target_date_uploaded_epi_count}"
            )
