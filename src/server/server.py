from flask import Flask, send_from_directory
from src.server.state import CheepPuzzleState
from src.server.word import Word
from src.server.category import Category
from src.server.player import CheepPlayerState
from flask_cors import CORS
import json
from cattrs import unstructure

app = Flask(__name__)
CORS(app)


@app.route("/init")
def init_puzzle_state():
    # here goes the code to return the initial game state
    category_one = Category.from_words("beverages", [Word("coffee"), Word("tea")])
    category_two = Category.from_words("inputs", [Word("keyboard"), Word("mouse")])
    puzzle_state = CheepPuzzleState.from_words_and_categories(
        categories=[category_one, category_two],
        words=[Word("coffee"), Word("tea"), Word("keyboard"), Word("mouse")],
    )
    return json.dumps(unstructure(puzzle_state), indent=4)

@app.route("/")
def error_incorrect_access():
    return "Error: Incorrect access"


# @app.route("/selection/<words>")
# def select():
#     return


def run():
    app.run(port=8000)
