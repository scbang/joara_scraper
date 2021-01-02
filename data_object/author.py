class JoaraAuthor(object):
    def __init__(self, member_id, member_nickname):
        self.member_id = member_id
        self.member_nickname = member_nickname

    def __str__(self):
        return f"{self.member_id}|{self.member_nickname}"


class RidibooksAuthor(object):
    def __init__(self, id, name, role, recent_published_book=None):
        self.id = id
        self.name = name
        self.role = role
        self.recent_published_book = recent_published_book

    def __str__(self):
        last_published_book_desc = \
            f"(이전 출간작 별점={self.recent_published_book['rating']['buyer_rating_score']}점 " \
            f"{self.recent_published_book['rating']['buyer_rating_count']}명)" \
                if self.recent_published_book else ""
        return f"{self.name}(ID={self.id}){last_published_book_desc}"
