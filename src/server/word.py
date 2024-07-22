from attrs import define


@define
class Word:
    data: str

    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
        return self.data
