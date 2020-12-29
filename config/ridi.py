import os
import re

RIDIBOOKS_HOST = "https://ridibooks.com"
ACCOUNT_ID = "kjk870624"
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")
LOGIN_URL = f"{RIDIBOOKS_HOST}/account/action/login"
ROMANCE_HOME = f"{RIDIBOOKS_HOST}/romance/"

CSS_SELECTOR = {
    "RECOMMENDATION": {
        "GET_LIST": re.compile("PortraitBookWrapper-todayRecommendationMargin$"),
    },
    "TODAY_NEW": {
        "GET_LIST": re.compile("PortraitBookWrapper-StyledBookItem$"),
    },
    "GET_BOOK_LINK": re.compile("StyledAnchor$"),
    "BOOK_LINK": {
        "TITLE": "info_title_wrap",
        "AUTHOR_DETAIL_LINK": "author_detail_link",
        "PUBLISHER_DETAIL_LINK": "publisher_detail_link",
        "STAR_RATE_SCORE": "StarRate_Score",
        "STAR_RATE_COUNT": "StarRate_ParticipantCount",
        "KEYWORDS": "keyword",
    },
}


def make_event_url(event_id):
    return f"{RIDIBOOKS_HOST}/event/{event_id}"
