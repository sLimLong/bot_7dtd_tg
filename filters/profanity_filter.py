import json
from aiogram import types
from aiogram.filters import Filter
from pathlib import Path

BAD_WORDS_PATH = Path("data/bad_words.json")

def load_bad_words():
    if BAD_WORDS_PATH.exists():
        with open(BAD_WORDS_PATH, "r", encoding="utf-8") as f:
            return set(word.lower() for word in json.load(f))
    return set()

class ProfanityFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        if not message.text:
            return False

        bad_words = load_bad_words()
        text = message.text.lower()

        return any(bad_word in text for bad_word in bad_words)
