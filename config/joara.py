HOST = "http://www.joara.com"
BASE_PATH = HOST + "/best/today_best_list.html"
FREE_QUERY = {
    "QUERY":         {
        "sl_subcategory": "series",
    },
    "PAGE_NO_LIST":  [1],
    "EPISODE_LIMIT": None,
}
LATELY_QUERY = {
    "QUERY":         {
        "sl_subcategory": "lately",
    },
    "PAGE_NO_LIST":  list(range(1, 6)),
    "EPISODE_LIMIT": 19,
}
COOKIES = {'best_favor_genre': '22'}  # 로맨스판타지
