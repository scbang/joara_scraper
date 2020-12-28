import requests
from bs4 import BeautifulSoup

import config


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
        requests.Request('POST', config.ridi.LOGIN_URL, headers=headers, data=payload))

    del login_request.headers['Connection']

    print(login_request.headers)
    print(login_request.body)
    login_response = ridi_session.send(login_request)
    if login_response.status_code == 200:
        print(f"Ridibooks successfully login with account ({user_id})")
    else:
        print(login_response.status_code)
        print(login_response.text)
        print(login_response.content)
        print(login_response)
        print("Ridibooks failed to login")
        ridi_session = None

    return ridi_session


def get_today_recommendation(session_obj):
    page = session_obj.get(config.ridi.ROMANCE_HOME)
    soup = BeautifulSoup(page.text, 'html.parser')

    recommendation_css_selector = config.ridi.CSS_SELECTOR["RECOMMENDATION"]
    list_selector = recommendation_css_selector["GET_LIST"]
    text_selector = recommendation_css_selector["GET_TEXT"]
    recommendation_list = soup.find_all(name="li", class_=list_selector)
    for recommendation_item in recommendation_list:
        # print(recommendation_item)
        print(recommendation_item.find(name="p", class_=text_selector).text)
