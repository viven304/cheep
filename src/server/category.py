from typing import List, Tuple
from src.server.word import Word
from attrs import define


@define
class Category:
    """
    A category contains the list of words that are a part of it
    """

    name: str
    words: List[Word]
    # color: Tuple[int, int, int] Maybe??

    @classmethod
    def from_words(cls, name, words):
        return cls(name, words)
