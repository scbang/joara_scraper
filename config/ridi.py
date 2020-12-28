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
        "GET_TEXT": re.compile("RecommendationText$"),
    },

}


def make_event_url(event_id):
    return f"{RIDIBOOKS_HOST}/event/{event_id}"
