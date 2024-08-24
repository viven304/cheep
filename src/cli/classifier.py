from src.models.bert import CategoriesClassifierBERT
import argparse
import sys


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Category classifier",
        description="Create 4 categories out of the words you provide",
    )
    parser.add_argument("words", nargs="*")
    return parser


def run():
    parser = setup_parser()
    opts = parser.parse_args()
    if not opts.words:
        print("Provide some words please")
        parser.print_help()
        sys.exit(1)
    if len(opts.words) % 4 != 0:
        raise ValueError("We need multiples of 4s number of words to classify")
    model = CategoriesClassifierBERT()
    model.cli_word_categorizer(opts.words)
