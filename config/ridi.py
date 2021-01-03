RIDIBOOKS_HOST = "https://ridibooks.com"
SEARCH_API_HOST = "https://search-api.ridibooks.com"
GET_BOOK_INFO_API_HOST = "https://book-api.ridibooks.com"
LOGIN_URL = f"{RIDIBOOKS_HOST}/account/action/login"
ROMANCE_HOME = f"{RIDIBOOKS_HOST}/romance/"
N_SCRAPE_WORKER = 10
N_SEARCH_RESULT_PER_PAGE = 24
PUBLISHER_SEARCH_API_URL = f"{SEARCH_API_HOST}/search"
SOUP_FIND_ARGS_GET_BOOK_DETAIL = {
    "TITLE_LINK": {
        "name": "a",
        "class_": "title_link",
        "href": True,
    },
    "STAR_RATE_SCORE": {
        "name": "span",
        "class_": "StarRate_Score"
    },
    "STAR_RATE_PARTICIPANT_COUNT": {
        "name": "span",
        "class_": "StarRate_ParticipantCount"
    },
}
SOUP_FIND_ARGS = {
    "GET_NEXT_DATA": {
        "name": "script",
        "id": "__NEXT_DATA__",
    },
    "BOOK_DETAIL_PAGE": {
        "PUBLISHER_DETAIL_LINK": {
            "name": "a",
            "class_": "publisher_detail_link"
        },
        "KEYWORDS": {
            "name": "span",
            "class_": "keyword"
        },
    },
    "EVENT_PAGE": {
        "GET_BOOK_LIST": {
            "name": "div",
            "class_": "book_metadata_wrapper"
        },
        "GET_BOOK_DETAIL": SOUP_FIND_ARGS_GET_BOOK_DETAIL,
    },
    "AUTHOR_DETAIL_PAGE": {
        "GET_BOOK_LIST": {
            "name": "div",
            "class_": "book_macro_landscape"
        },
        "GET_BOOK_DETAIL": SOUP_FIND_ARGS_GET_BOOK_DETAIL,
    },
}

DEFAULT_RESULT_XLSX_FILE_NAME = "리디북스_로맨스_e북_정리.xlsx"
excludes_for_today_recommendation = ['today_new_list', 'event_books']
excludes_for_event = ['today_recommendation_list', 'today_new_list']
BOOK_DATA_HEADERS = [
    ("순서", "i+1", True, []),
    ("작품 제목", "book_detail.title", True, []),
    ("출판사 이름", "book_detail.publisher", True, []),
    ("작가 이름", "author.name", False, []),
    ("최근 출간작 제목", "recent_published_book['title'] if recent_published_book else ''", False,
     excludes_for_today_recommendation),
    ("최근 출간작 링크", "recent_published_book['link'] if recent_published_book else ''", False,
     excludes_for_today_recommendation),
    ("최근 출간작 별점", "recent_published_book['rating']['buyer_rating_score'] if recent_published_book else ''", False,
     excludes_for_today_recommendation),
    ("최근 출간작 별점수", "recent_published_book['rating']['buyer_rating_count'] if recent_published_book else ''", False,
     excludes_for_today_recommendation),
    ("작가 ID", "author.id", False, []),
    ("작가 Role", "author.role", False, []),
    ("작품 별점", "book_detail.start_rate", True, []),
    ("작품 별점 참여수", "book_detail.star_rate_participants_count", True, []),
    ("작품 키워드", "book_detail.keywords_to_str()", True, []),
    ("작품 ID", "book_detail.book_id", True, []),
    ("작품 링크", "book_detail.link", True, []),
    ("오리발 노출 여부", "found_in_today_recommendation", True, excludes_for_event),
    ("오신 노출 여부", "found_in_today_new", True, excludes_for_event),
]
PUBLISHER_DETAIL_HEADERS = [
    ("출판사 이름", "publisher_obj['publisher'].publisher_name"),
    ("출판사 ID", "publisher_obj['publisher'].publisher_id"),
    ("출판사 CP 이름", "publisher_obj['publisher'].cp_name"),
    ("최근 30일간 출간 종수", "publisher_obj['published_recent_30_days']['count']"),
    ("수집 시각", "publisher_obj['published_recent_30_days']['now'].isoformat()"),
]


def make_url(url):
    return f"{RIDIBOOKS_HOST}{url}"


def make_event_url(event_id):
    return f"{RIDIBOOKS_HOST}/event/{event_id}"


def make_book_url(book_id):
    return f"{RIDIBOOKS_HOST}/books/{book_id}"


def make_book_api_url(book_id):
    return f"{GET_BOOK_INFO_API_HOST}/books/{book_id}"


def make_author_url(author_id):
    return f"{RIDIBOOKS_HOST}/author/{author_id}"
