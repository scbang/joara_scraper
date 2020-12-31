import os

RIDIBOOKS_HOST = "https://ridibooks.com"
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")
LOGIN_URL = f"{RIDIBOOKS_HOST}/account/action/login"
ROMANCE_HOME = f"{RIDIBOOKS_HOST}/romance/"

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
        "GET_BOOK_DETAIL": {
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
            "AUTHOR_DETAIL_LINK": {
                "name": "a",
                "class_": "author_detail_link",
                "href": True,
            },
        },
    },
}


def make_url(url):
    return f"{RIDIBOOKS_HOST}{url}"


def make_event_url(event_id):
    return f"{RIDIBOOKS_HOST}/event/{event_id}"


def make_book_url(book_id):
    return f"{RIDIBOOKS_HOST}/books/{book_id}"
