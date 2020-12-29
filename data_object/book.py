from enum import Enum

from config import RIDIBOOKS_HOST


class Platform(Enum):
    JOARA = "조아라"
    RIDIBOOKS = "리디북스"

    def __str__(self):
        return self.value


class Book(object):
    def __init__(self, platform, book_id, title, authors, publishers):
        self.platform = platform
        self.book_id = book_id
        self.title = title
        self.authors = authors
        self.publishers = publishers

    def __str__(self):
        return f"ID = {self.book_id}" \
               f", 플랫폼 = {self.platform}" \
               f", 제목 = {self.title}" \
               f", 작가 = [{', '.join(map(str, self.authors))}]" \
               f", 출판사 = [{', '.join(map(str, self.publishers))}]"


class RidibooksBook(Book):
    def __init__(self, link, star_rate_participants_count, start_rate, title, authors, publishers, keywords):
        book_id = link.split("/")[-1]
        super().__init__(Platform.RIDIBOOKS, book_id, title, authors, publishers)
        self.link = f"{RIDIBOOKS_HOST}{link}"
        self.star_rate_participants_count = star_rate_participants_count
        self.start_rate = start_rate
        self.keywords = keywords

    def __str__(self):
        return f"{str(super().__str__())}" \
               f", 링크 = {self.link}" \
               f", 별점수 = {self.star_rate_participants_count}" \
               f", 별점 = {self.start_rate}" \
               f", 키워드 = [{', '.join(map(str, self.keywords))}]"
