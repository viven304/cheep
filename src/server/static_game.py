"""
Module that provides you just re-shuffled examples from past games
"""
import json
import random
import typing
from src.server.category import Category
from src.server.word import Word

def get_four_random_categories() -> typing.Iterable[Category]:
    with open("./data/answers.json", "r") as f:
        past_answers = json.load(f)
    n = 4
    num_answers = len(past_answers)
    raw_categories = []
    while n > 0:
        raw_categories.append(past_answers[random.randrange(0, num_answers - 1)])
        n -= 1
    game_categories = []
    game_words = []
    for raw_category in raw_categories:
        words = [Word(word_txt) for word_txt in raw_category["words"]]
        game_categories.append(Category(raw_category["category"], words))
        for word in words:
            game_words.append(word)
    random.shuffle(game_words)
    return game_categories, game_words