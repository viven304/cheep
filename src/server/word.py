from attrs import define


@define
class Word:
    data: str

    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    def __repr__(self):
        return self.data

    def __lt__(self, other):
        return self.data < other.data