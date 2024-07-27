from flask import Flask, request, jsonify
from src.server.state import CheepPuzzleState
from src.server.word import Word
from src.server.category import Category
from src.server.player import CheepPlayerState
from flask_cors import CORS
import json
from cattrs import unstructure, structure
import typing

app = Flask(__name__)
CORS(app)

category_one = Category.from_words("beverages", [Word("coffee"), Word("tea")])
category_two = Category.from_words("inputs", [Word("keyboard"), Word("mouse")])
puzzle_state = CheepPuzzleState.from_words_and_categories(
    categories=[category_one, category_two],
    words=[Word("coffee"), Word("tea"), Word("keyboard"), Word("mouse")],
)
@app.route("/puzzle/state/init")
def init_puzzle_state():
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
    return puzzle_state.verify_selected_words(words);

@app.route("/selection", methods=["POST"])
def verifySelection():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return jsonify({'message': 'Data received', 'validation_result': _validateAnswer(json)})
    else:
        return 'Content-Type not supported!'


def run():
    app.run(port=8000)
