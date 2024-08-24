from src.models.bert import CategoriesClassifierBERT
import argparse
import sys


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Fine-tune a",
        description="Fine-tune a BERT classifier with connections data",
    )
    return parser


def run():
    parser = setup_parser()
    _ = parser.parse_args()
    model = CategoriesClassifierBERT()
    model.train()
