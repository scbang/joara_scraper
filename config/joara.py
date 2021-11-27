JOARA_HOST = "http://pre.joara.com"
BASE_PATH = JOARA_HOST + "/best/today_best_list.html"
FREE_QUERY = {
    "QUERY": {
        "sl_subcategory": "series",
    },
    # "PAGE_NO_LIST": list(range(1, 2)),
    "PAGE_NO_LIST": list(range(1, 6)),
    "EPISODE_LIMIT": None,
}
LATELY_QUERY = {
    "QUERY": {
        "sl_subcategory": "lately",
    },
    # "PAGE_NO_LIST": list(range(1, 2)),
    "PAGE_NO_LIST": list(range(1, 6)),
    "EPISODE_LIMIT": 19,
}
COOKIES = {'best_favor_genre': '22'}  # 로맨스판타지
CSS_SELECTOR = {
    "NORMAL": {
        "BOOK_INFO": ".txt_c_sty01 > .info_c > .info2 > .date",
        "EPISODE_DETAIL": ".tbl_work > tbody > tr",
        "CELL": "td.chapter_cell",
    },
    "NOBLESS": {
        "BOOK_INFO": ".flistCon",
        "EPISODE_DETAIL": ".partList",
        "CELL": ".partListInfo",
    },
}
DEFAULT_RESULT_XLSX_FILE_NAME = "조아라_투베분석.xlsx"
DEFAULT_ANALYZED_XLSX_FILE_NAME = "조아라_투베분석_정리.xlsx"

DATA_HEADERS = [
    "랭킹",
    "작가 ID",
    "작가 닉네임",
    "수집 날짜",
    "작품 코드",
    "제목",
    "최근연재회차",
    "수집 날짜 최신 연재회차",
    "투데이 베스트지수",
    "투데이 선작",
    "투데이 추천",
    "투데이 조회",
    "작품 전체 추천수",
    "작품 전체 선작",
    "첫회 조회수",
    "수집 날짜 조회수",
    "수집 날짜 연재 회차수",
    "선작비",
    "연독률",
    "추천비",
    "회당 선작수",
    "장르",
    "소개글",
]

ALWAYS_ANALYZE_BOOK_CODE_LIST = [
    1379253,  # 폭군아빠가 된다면
]
