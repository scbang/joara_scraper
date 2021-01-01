import json
import queue
import time
from datetime import datetime
from multiprocessing import Process, Queue
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

import config
from config import make_url
from data_object.book import RidibooksBook


def login(
        user_id: int or str,
        user_password: str,
) -> requests.Session:
    session_obj = requests.Session()

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
    login_request = session_obj.prepare_request(
        requests.Request('POST', config.ridi.LOGIN_URL, headers=headers, data=payload)
    )

    call_with_response_check("리디북스 로그인", 200, session_obj.send, login_request)
    return session_obj


def call_with_response_check(
        request_description: str,
        expected_status_code: int,
        func: callable,
        *args,
        **kwargs
) -> requests.Response:
    response = func(*args, **kwargs)
    if response.status_code != expected_status_code:
        print(f"{request_description} 요청 실패")
        print(f"응답 코드 = {response.status_code}, 기대값 = {expected_status_code}")
        raise Exception(f"{request_description} 요청 실패")
    return response


def get_book_detail(
        session_obj: requests.Session,
        book_info: Dict,
) -> RidibooksBook:
    book_link = config.make_book_url(book_info['b_id'])

    book_link_response = call_with_response_check(f"{book_link} 읽기", 200, session_obj.get, book_link)
    book_detail_soup = BeautifulSoup(book_link_response.text, 'html.parser')

    book_link_find_args = config.ridi.SOUP_FIND_ARGS["BOOK_DETAIL_PAGE"]

    publisher_detail_link_selector = book_link_find_args["PUBLISHER_DETAIL_LINK"]
    keywords_selector = book_link_find_args["KEYWORDS"]

    return RidibooksBook(
        link=book_link,
        star_rate_participants_count=book_info["rating"]["buyer_rating_count"],
        start_rate=book_info["rating"]["buyer_rating_score"],
        title=book_info["title"],
        authors=[author['name'] for author in book_info['authors']],
        publisher=book_detail_soup.find(**publisher_detail_link_selector).text,
        keywords=[keywords_span.text for keywords_span in book_detail_soup.find_all(**keywords_selector)],
    )


def scrape_worker(
        worker_id: int,
        book_info_list: List,
        scrape_result: Queue,
):
    with login(config.ACCOUNT_ID, config.ACCOUNT_PASSWORD) as session_obj:
        for book_info in book_info_list:
            print(f"스크랩 워커({worker_id}) {config.make_book_url(book_info['b_id'])} 수집 중")
            scrape_result.put((book_info["b_id"], get_book_detail(session_obj, book_info)))
    print(f"스크랩 워커({worker_id}) 수집 완료")


def scrape_event(
        session_obj: requests.Session,
        event_info: Dict,
) -> List:
    event_url = config.make_url(event_info['url'])
    event_page = call_with_response_check(f"이벤트[{event_info['title']}] 페이지 읽기", 200, session_obj.get, event_url)
    event_detail_soup = BeautifulSoup(event_page.text, 'html.parser')

    event_link_find_args = config.ridi.SOUP_FIND_ARGS["EVENT_PAGE"]
    get_book_detail_find_args = event_link_find_args["GET_BOOK_DETAIL"]

    event_book_items = []

    for i, event_book in enumerate(event_detail_soup.find_all(**event_link_find_args["GET_BOOK_LIST"])):
        title_html = event_book.find(**get_book_detail_find_args["TITLE_LINK"])
        title_link = title_html['href']

        event_book_item = {
            "b_id": title_link.split('/')[-1],
            "title": title_html.text.strip(),
            "rating": {
                "buyer_rating_score":
                    event_book.find(**get_book_detail_find_args["STAR_RATE_SCORE"]).text.split("점")[0]
                    if event_book.find(**get_book_detail_find_args["STAR_RATE_SCORE"]) else "0"
                ,
                "buyer_rating_count":
                    event_book.find(**get_book_detail_find_args["STAR_RATE_PARTICIPANT_COUNT"]).text.split("명")[0]
                    if event_book.find(**get_book_detail_find_args["STAR_RATE_PARTICIPANT_COUNT"]) else "0",
            },
            "authors": [
                {
                    "name": event_book.find(**get_book_detail_find_args["AUTHOR_DETAIL_LINK"]).text,
                }
            ],
        }
        event_book_items.append(event_book_item)

    return event_book_items


def find_book_infos_in_next_data(
        session_obj: requests.Session,
        next_data: Dict,
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    branches = next_data["props"]["initialProps"]["pageProps"]["branches"]

    top_banner_events = []
    today_new_list = []
    today_recommendation_list = []
    for branch in branches:
        if branch["slug"] == "home-romance-event-banner-top":
            top_banner_events = branch["items"][0:min(4, len(branch["items"]))]
        elif branch["slug"] == "home-romance-today-new-book":
            today_new_list = branch["items"]
        elif branch["slug"] == "home-romance-today-recommendation":
            today_recommendation_list = branch["items"]

    if today_recommendation_list:
        print("+++ [오늘, 리디의 발견] 영역 데이터 발견")

    if today_new_list:
        print("+++ [오늘의 신간] 영역 데이터 발견")

    event_books = list()
    if top_banner_events:
        print(f"+++ 최상단 배너 영역 데이터 발견. {len(top_banner_events)}개 이벤트 노출 중.")
        for top_banner_event in top_banner_events:
            event_books.append({
                "book_items": scrape_event(session_obj, top_banner_event),
                "event_info": top_banner_event,
            })

    return today_recommendation_list, today_new_list, event_books


def make_n_array(
        today_recommendation_list: List[Dict],
        today_new_list: List[Dict],
        event_books: List[Dict],
        n_book_detail_scrape_worker_process: int,
) -> List[List[Dict]]:
    book_item_lists = [[] for i in range(n_book_detail_scrape_worker_process)]

    n = 0
    for today_recommendation in today_recommendation_list:
        book_item_lists[n % n_book_detail_scrape_worker_process].append(today_recommendation)
        # print([len(book_item_list) for book_item_list in book_item_lists])
        n += 1
    for today_new in today_new_list:
        book_item_lists[n % n_book_detail_scrape_worker_process].append(today_new)
        n += 1
    for event_book in event_books:
        for book_item in event_book["book_items"]:
            book_item_lists[n % n_book_detail_scrape_worker_process].append(book_item)
            n += 1

    return book_item_lists


def get_book_details(
        book_item_lists: List[List[Dict]],
) -> Dict:
    book_details = dict()

    scrape_processes = []
    scrape_result_queue = Queue()

    for i, book_item_list in enumerate(book_item_lists):
        print(f"스크랩 워커({i}) 시작...")
        # print(f"{[book_item['b_id'] for book_item in book_item_list]}")
        process = Process(target=scrape_worker, args=(i, book_item_list, scrape_result_queue,))
        process.start()
        scrape_processes.append(process)

    alive_procs = list(scrape_processes)
    while alive_procs:
        try:
            while 1:
                scrape_result = scrape_result_queue.get(False)
                book_details[scrape_result[0]] = scrape_result[1]
        except queue.Empty:
            pass

        time.sleep(0.5)  # Give tasks a chance to put more data in
        if not scrape_result_queue.empty():
            continue
        alive_procs = [p for p in alive_procs if p.is_alive()]

    for i, scrape_process in enumerate(scrape_processes):
        print(f"스크랩 워커({i}) 종료 대기")
        scrape_process.join()

    print(f"+++ 스크랩 종료...{len(book_details)}개의 책 페이지 데이터 수집 완료")

    return book_details


def print_scrape_result(
        book_details: dict,
        today_recommendation_list: list,
        today_new_list: list,
        event_books: list,
) -> None:
    if today_recommendation_list:
        print("")
        print(f"+++ [오늘, 리디의 발견] 수집 결과, {len(today_recommendation_list)}개의 책 페이지 발견")
        for i, today_recommendation in enumerate(today_recommendation_list):
            print(f"{i+1}번째 책, {book_details[today_recommendation['b_id']]}")

    if today_new_list:
        print("")
        print(f"+++ [오늘의 신간] 수집 결과, {len(today_new_list)}개의 책 페이지 발견")
        for i, today_new in enumerate(today_new_list):
            print(f"{i+1}번째 책, {book_details[today_new['b_id']]}")

    if event_books:
        print("")
        print(f"+++ 최상단 배너 영역 발견 수집 결과. {len(event_books)}개 이벤트 노출 중.")
        for i, item in enumerate(event_books):
            top_banner_event = item["event_info"]
            event_book_list = item["book_items"]
            print(f"--- {i+1}번째 이벤트, [{top_banner_event['title']}]"
                  f", 링크 = {make_url(top_banner_event['url'])}"
                  f", {len(event_book_list)}개의 책 페이지 발견")
            for nth, event_book in enumerate(event_book_list):
                print(f"{nth+1}번째 책, {book_details[event_book['b_id']]}")


def scrape_romance_home():
    print(f"+++ 리디북스 로맨스 데이터 수집기 - 실행일시 : {str(datetime.now())[0:19]}"
          f", 수집 페이지 링크 = {config.ridi.ROMANCE_HOME}")

    session_obj = login(config.ACCOUNT_ID, config.ACCOUNT_PASSWORD)
    romance_response = call_with_response_check("로맨스 페이지 읽기", 200, session_obj.get, config.ridi.ROMANCE_HOME)

    today_recommendation_list, today_new_list, event_books = find_book_infos_in_next_data(
        session_obj,
        json.loads(
            BeautifulSoup(romance_response.text, 'html.parser')
                .find(**config.ridi.SOUP_FIND_ARGS["GET_NEXT_DATA"])
                .text
        )
    )

    print_scrape_result(
        get_book_details(make_n_array(today_recommendation_list, today_new_list, event_books, 10)),
        today_recommendation_list,
        today_new_list,
        event_books,
    )
