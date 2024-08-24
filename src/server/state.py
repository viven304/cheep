from src.server.word import Word
from src.server.category import Category
from typing import List, Tuple
from attrs import define


@define
class CheepPuzzleState:
    """
    Cheep game state that track all the elements 
    that can be affected by player action
    
    :param words: List of words in the game
    """

    words: List[Word]
    solved_categories: List[Category]
    unsolved_categories: List[Category]

    @classmethod
    def from_words_and_categories(cls, words, categories):
        """
        Initialize game state with a list of words and categories
        """
        return cls(words=words, solved_categories=[], unsolved_categories=categories)

    @classmethod
    def from_save(cls):
        """
        Load game state from a cached save file
        """
        return

    def verify_selected_words(self, selected_words: List[Word]) -> Tuple[Category, bool]:
        for category in self.unsolved_categories:
            if sorted(category.words) == sorted(selected_words):
                self.mark_correct(category)
                return category, True

        for category in self.solved_categories:
            if category.words == selected_words:
                return category, False
        return None, False

    def mark_correct(self, selected_category):
        """
        Mark selected category as correct
        """
        for category in self.unsolved_categories:
            if category.name == selected_category.name:
                self.solved_categories.append(category)
                self.unsolved_categories.remove(category)

    def reset(self):
        """
        Reset the puzzle state to the default starting state
        """
        total_categories = self.solved_categories + self.unsolved_categories
        self.solved_categories = []
        self.unsolved_categories = total_categories
