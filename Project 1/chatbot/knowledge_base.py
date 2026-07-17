from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Any
from chatbot.exceptions import KnowledgeBaseError
logger = logging.getLogger('decodebot.knowledge_base')

class KnowledgeBase:
    REQUIRED_KEYS = {'intents', 'exit_commands', 'default_response'}

    def __init__(self, source_path: str | Path) -> None:
        self.source_path = Path(source_path)
        self.intents: dict[str, list[str]] = {}
        self.exit_commands: set[str] = set()
        self.default_response: str = 'I do not understand that yet.'
        self._load()

    def _load(self) -> None:
        if not self.source_path.exists():
            raise KnowledgeBaseError(f'Knowledge base file not found: {self.source_path}')
        try:
            raw_text = self.source_path.read_text(encoding='utf-8')
            data: dict[str, Any] = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise KnowledgeBaseError(f'Knowledge base file is not valid JSON: {exc}') from exc
        missing = self.REQUIRED_KEYS - data.keys()
        if missing:
            raise KnowledgeBaseError(f'Knowledge base is missing required keys: {sorted(missing)}')
        intents_raw = data['intents']
        if not isinstance(intents_raw, dict) or not intents_raw:
            raise KnowledgeBaseError('Knowledge base must define at least one intent.')
        for intent_key, intent_value in intents_raw.items():
            responses = intent_value.get('responses')
            if not responses or not isinstance(responses, list):
                raise KnowledgeBaseError(f"Intent '{intent_key}' must define a non-empty 'responses' list.")
            self.intents[intent_key] = responses
        self.exit_commands = set(data['exit_commands'])
        self.default_response = data['default_response']
        logger.info('Knowledge base loaded: %d intents, %d exit commands.', len(self.intents), len(self.exit_commands))

    def get_responses(self, key: str) -> list[str] | None:
        return self.intents.get(key)

    def is_exit_command(self, key: str) -> bool:
        return key in self.exit_commands
