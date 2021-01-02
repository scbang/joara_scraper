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
