from flask import Flask, request, jsonify
from src.server.state import CheepPuzzleState
from src.server.word import Word
from src.server.category import Category
from src.server.player import CheepPlayerState
from src.server.static_game import get_four_random_categories
from flask_cors import CORS
import json
from cattrs import unstructure, structure
import typing

app = Flask(__name__)
CORS(app)

categories, words = get_four_random_categories()
puzzle_state = CheepPuzzleState.from_words_and_categories(
    categories=categories,
    words=words,
)


@app.route("/puzzle/state/init")
def init_puzzle_state():
    puzzle_state.reset()
    return json.dumps(unstructure(puzzle_state), indent=4)


@app.route("/player/state/init")
def player_state():
    player_state = CheepPlayerState()
    return json.dumps(unstructure(player_state), indent=4)


@app.route("/")
def error_incorrect_access():
    return "Error: Incorrect access"


def _validateAnswer(json):
    selection = json["data"]
    words = structure(selection, typing.List[Word])
    print(f"selected: {words}")
    return puzzle_state.verify_selected_words(words)


@app.route("/selection", methods=["POST"])
def verifySelection():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = request.json
        category, is_correct = _validateAnswer(json)
        print(f"Is it the right answer?: {is_correct}")
        return jsonify(
            {"category": unstructure(category), "validation_result": is_correct}
        )
    else:
        return "Content-Type not supported!"


def run():
    app.run(port=8000)
