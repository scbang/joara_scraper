class Author(object):
    def __init__(self, member_id, member_nickname):
        self.member_id = member_id
        self.member_nickname = member_nickname

    def __str__(self):
        return f"{self.member_id}|{self.member_nickname}"

