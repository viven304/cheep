from attrs import define
from typing import List
from src.server.category import Category


@define
class CheepPlayerState:
    completed_categories: List[Category]
    mistakes: int

    def __init__(self, mistakes=3):
        self.completed_categories = []
        self.mistakes = mistakes

    @classmethod
    def from_completed_categories(cls, categories):
        return cls(completed_categories=categories)

    @classmethod
    def from_save(cls):
        return
