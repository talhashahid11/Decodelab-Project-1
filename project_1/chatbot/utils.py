from __future__ import annotations
from chatbot.exceptions import EmptyInputError

def sanitize_input(raw_input: str) -> str:
    if raw_input is None:
        raise EmptyInputError('Input cannot be None.')
    cleaned = ' '.join(raw_input.strip().split()).lower()
    if not cleaned:
        raise EmptyInputError('Input cannot be blank.')
    return cleaned
