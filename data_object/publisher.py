class Publisher(object):
    def __init__(self, publisher_id, publisher_name, cp_name):
        self.publisher_id = publisher_id
        self.publisher_name = publisher_name
        self.cp_name = cp_name

    def __str__(self):
        return f"ID = {self.publisher_id}" \
               f", 이름 = {self.publisher_name}" \
               f", CP 이름 = {self.cp_name}"
