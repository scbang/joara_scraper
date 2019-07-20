import requests
from bs4 import BeautifulSoup

import config
from data_object.author import Author


def get_list():
    print(config.URL)
    page = requests.get(config.URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    tbl_list = soup.select(".tbl_list > tbody > tr")
    top_raning = 1
    for tr in tbl_list:
        td_list = tr.select("td")
        if 'class' in tr.attrs and 'top_ranking' in tr.attrs['class']:
            ranking = top_raning
            top_raning += 1
        else:
            ranking = int(td_list[0].text.strip())
        author_elem = td_list[1].select(".member_nickname")
        author_member_id = author_elem[0].attrs["member_id"]
        author_member_nickname = author_elem[0].text.strip()
        author = Author(author_member_id, author_member_nickname)
        print("랭킹 {}위, {}".format(ranking, author))


    print(len(tbl_list))

