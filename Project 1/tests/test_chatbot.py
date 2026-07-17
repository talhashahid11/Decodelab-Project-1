from __future__ import annotations
import json
from pathlib import Path
import pytest
from chatbot.bot import ChatBot
from chatbot.exceptions import EmptyInputError, KnowledgeBaseError
from chatbot.knowledge_base import KnowledgeBase
from chatbot.utils import sanitize_input

@pytest.fixture
def kb_file(tmp_path: Path) -> Path:
    data = {'intents': {'hello': {'responses': ['Hi!']}, 'bye': {'responses': ['Goodbye!']}, 'time': {'responses': ['__DYNAMIC_TIME__']}}, 'exit_commands': ['exit', 'quit', 'bye'], 'default_response': 'I do not understand.'}
    path = tmp_path / 'kb.json'
    path.write_text(json.dumps(data), encoding='utf-8')
    return path

@pytest.fixture
def bot(kb_file: Path) -> ChatBot:
    return ChatBot(knowledge_base=KnowledgeBase(kb_file))

class TestSanitizeInput:

    def test_lowercases_text(self):
        assert sanitize_input('HELLO') == 'hello'

    def test_strips_whitespace(self):
        assert sanitize_input('  hello  ') == 'hello'

    def test_collapses_internal_whitespace(self):
        assert sanitize_input('hello    world') == 'hello world'

    def test_raises_on_empty_string(self):
        with pytest.raises(EmptyInputError):
            sanitize_input('   ')

    def test_raises_on_none(self):
        with pytest.raises(EmptyInputError):
            sanitize_input(None)

class TestKnowledgeBase:

    def test_loads_valid_file(self, kb_file: Path):
        kb = KnowledgeBase(kb_file)
        assert 'hello' in kb.intents
        assert kb.default_response == 'I do not understand.'

    def test_missing_file_raises(self, tmp_path: Path):
        with pytest.raises(KnowledgeBaseError):
            KnowledgeBase(tmp_path / 'does_not_exist.json')

    def test_invalid_json_raises(self, tmp_path: Path):
        bad_file = tmp_path / 'bad.json'
        bad_file.write_text('{not valid json', encoding='utf-8')
        with pytest.raises(KnowledgeBaseError):
            KnowledgeBase(bad_file)

    def test_missing_required_keys_raises(self, tmp_path: Path):
        bad_file = tmp_path / 'bad.json'
        bad_file.write_text(json.dumps({'intents': {'hi': {'responses': ['hey']}}}), encoding='utf-8')
        with pytest.raises(KnowledgeBaseError):
            KnowledgeBase(bad_file)

    def test_is_exit_command(self, kb_file: Path):
        kb = KnowledgeBase(kb_file)
        assert kb.is_exit_command('exit') is True
        assert kb.is_exit_command('hello') is False

class TestChatBot:

    def test_known_intent_returns_correct_response(self, bot: ChatBot):
        response, should_exit = bot.respond('Hello')
        assert response == 'Hi!'
        assert should_exit is False

    def test_case_and_whitespace_insensitive(self, bot: ChatBot):
        response, _ = bot.respond('   HELLO   ')
        assert response == 'Hi!'

    def test_unknown_intent_returns_default(self, bot: ChatBot):
        response, should_exit = bot.respond('asdkjhasd')
        assert response == 'I do not understand.'
        assert should_exit is False

    def test_exit_command_flags_exit(self, bot: ChatBot):
        _, should_exit = bot.respond('exit')
        assert should_exit is True

    def test_bye_is_both_response_and_exit(self, bot: ChatBot):
        response, should_exit = bot.respond('bye')
        assert response == 'Goodbye!'
        assert should_exit is True

    def test_empty_input_does_not_crash(self, bot: ChatBot):
        response, should_exit = bot.respond('   ')
        assert should_exit is False
        assert 'type something' in response.lower()

    def test_dynamic_time_marker_resolved(self, bot: ChatBot):
        response, _ = bot.respond('time')
        assert 'current time is' in response.lower()

    def test_turn_count_increments(self, bot: ChatBot):
        bot.respond('hello')
        bot.respond('hello')
        assert bot.turn_count == 2
