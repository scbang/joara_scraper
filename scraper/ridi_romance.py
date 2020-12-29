import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import config
from data_object.book import RidibooksBook


def login(user_id, user_password):
    ridi_session = requests.Session()

    headers = {
        # 'accept': 'application/json, text/plain, */*',
        # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        # 'cookie': '__cfduid=d44a77019c07df334605dec2e6d349ad01609142992; user_device_type=PC; fantasy_main_genre=fantasy; bl_main_genre=bl_novel; comic_main_genre=comic; PHPSESSID=ltj8tfqpbvlkrhmn6ehev4unr8; adult_exclude=n; ruid=96697f8f-ruid-407f-bf3f-87e602d644ac; _gid=GA1.2.1185536721.1609142994; _fbp=fb.1.1609142994063.1110465508; ab.storage.deviceId.1440c75a-6f4b-48d9-8e69-8d6fd78a9fbc=%7B%22g%22%3A%22dd6c9577-7559-7fc9-0d05-dd4abf57fd8e%22%2C%22c%22%3A1609143080795%2C%22l%22%3A1609143080795%7D; ab.storage.userId.1440c75a-6f4b-48d9-8e69-8d6fd78a9fbc=%7B%22g%22%3A%22239326%22%2C%22c%22%3A1609143085512%2C%22l%22%3A1609143085512%7D; main_genre=romance; romance_main_genre=romance; _gat=1; pvid=b994eb75-pvid-4f2c-9e1d-593dbddfddbc; wcs_bt=s_116898344f34:1609162826; _ga_YB9VX70336=GS1.1.1609162802.2.1.1609162826.0; _ga=GA1.1.1380457973.1609142994; ab.storage.sessionId.1440c75a-6f4b-48d9-8e69-8d6fd78a9fbc=%7B%22g%22%3A%2223498491-0fd1-dd21-2927-780b5f66bcf3%22%2C%22e%22%3A1609164626710%2C%22c%22%3A1609162803755%2C%22l%22%3A1609162826710%7D',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'origin': 'https://ridibooks.com',
        # 'referer': 'https://ridibooks.com/account/login?return_url=https%3A%2F%2Fridibooks.com%2Fromance%2F',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
    }
    payload = {
        'user_id': user_id,
        'password': user_password,
        'cmd': 'login',
        'return_url': '',
        'return_query_string': '',
        'device_id': '',
        'msg': '',
    }
    login_request = ridi_session.prepare_request(
        requests.Request('POST', config.ridi.LOGIN_URL, headers=headers, data=payload)
    )

    call_with_response_check("리디북스 로그인", 200, ridi_session.send, login_request)
    return ridi_session


def call_with_response_check(request_description, expected_status_code, func, *args, **kwargs):
    response = func(*args, **kwargs)
    if response.status_code != expected_status_code:
        print(f"{request_description} 요청 실패")
        print(f"응답 코드 = {response.status_code}, 기대값 = {expected_status_code}")
        raise Exception(f"{request_description} 요청 실패")
    return response


def get_book_detail(session_obj, book_item):
    book_link_css_selector = config.ridi.CSS_SELECTOR["BOOK_LINK"]

    get_book_link_selector = config.ridi.CSS_SELECTOR["GET_BOOK_LINK"]
    title_selector = book_link_css_selector["TITLE"]
    author_detail_link_selector = book_link_css_selector["AUTHOR_DETAIL_LINK"]
    publisher_detail_link_selector = book_link_css_selector["PUBLISHER_DETAIL_LINK"]
    star_rate_score_selector = book_link_css_selector["STAR_RATE_SCORE"]
    star_rate_count_selector = book_link_css_selector["STAR_RATE_COUNT"]
    keywords_selector = book_link_css_selector["KEYWORDS"]

    book_link = book_item.find(name="a", class_=get_book_link_selector).attrs['href']

    book_link_response = call_with_response_check(
        f"{book_link} 읽기", 200, session_obj.get, f"{config.ridi.RIDIBOOKS_HOST}{book_link}"
    )
    # print(book_link_response)
    book_detail_soup = BeautifulSoup(book_link_response.text, 'html.parser')

    star_rate_score_span = book_detail_soup.find(name="span", class_=star_rate_score_selector)
    star_rate_count_span = book_detail_soup.find(name="span", class_=star_rate_count_selector)

    title = book_detail_soup.find(name="h3", class_=title_selector).text
    author_name = book_detail_soup.find(name="a", class_=author_detail_link_selector).text
    publisher_name = book_detail_soup.find(name="a", class_=publisher_detail_link_selector).text
    star_rate_score = star_rate_score_span.text if star_rate_score_span else "-"
    star_rate_count = star_rate_count_span.text if star_rate_count_span else "0명"

    keywords = [
        keywords_span.text
        for keywords_span in book_detail_soup.find_all(name="span", class_=keywords_selector)
    ]

    return RidibooksBook(
        book_link,
        star_rate_count,
        star_rate_score,
        title,
        [author_name, ],
        [publisher_name, ],
        keywords
    )


def get_today_recommendation(session_obj):
    print(f"리디북스 로맨스 데이터 수집기 - 실행일시 : {str(datetime.now())[0:19]}")

    romance_response = call_with_response_check("로맨스 페이지 읽기", 200, session_obj.get, config.ridi.ROMANCE_HOME)
    soup = BeautifulSoup(romance_response.text, 'html.parser')

    recommendation_list_selector = config.ridi.CSS_SELECTOR["RECOMMENDATION"]["GET_LIST"]

    recommendation_list = soup.find_all(name="li", class_=recommendation_list_selector)
    print("오리발 데이터 수집")
    for i, recommendation_item in enumerate(recommendation_list):
        print(f"{i+1}번째, {get_book_detail(session_obj, recommendation_item)}")

    print("오늘의 신간 데이터 수집")
    section_list = soup.find_all(name="section", class_=re.compile("SectionWrapper$"))
    today_new_section = None
    for i, section_item in enumerate(section_list):
        h2 = section_item.find(name="h2")
        a = h2.find(name="a")
        if a and a.text.startswith("오늘의 신간"):
            today_new_section = section_item

    if not today_new_section:
        print("오늘의 신간 영역 추출 실패")
        return

    today_new_list_selector = config.ridi.CSS_SELECTOR["TODAY_NEW"]["GET_LIST"]
    today_new_list = today_new_section.find_all(name="li", class_=today_new_list_selector)
    for i, today_new_item in enumerate(today_new_list):
        print(f"{i+1}번째, {get_book_detail(session_obj, today_new_item)}")
