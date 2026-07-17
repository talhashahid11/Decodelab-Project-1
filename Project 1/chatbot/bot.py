from __future__ import annotations
import logging
import random
from datetime import datetime
from chatbot.exceptions import EmptyInputError
from chatbot.knowledge_base import KnowledgeBase
from chatbot.utils import sanitize_input
logger = logging.getLogger('decodebot.bot')
DYNAMIC_TIME_MARKER = '__DYNAMIC_TIME__'

class ChatBot:

    def __init__(self, knowledge_base: KnowledgeBase, name: str='DecodeBot') -> None:
        self.name = name
        self.kb = knowledge_base
        self.turn_count = 0
        logger.info('%s initialized.', self.name)

    def respond(self, raw_user_input: str) -> tuple[str, bool]:
        try:
            clean_input = sanitize_input(raw_user_input)
        except EmptyInputError:
            logger.debug('Empty input received; prompting user again.')
            return ('Please type something so I can help you.', False)
        self.turn_count += 1
        logger.debug('Turn %d | user input (sanitized): %r', self.turn_count, clean_input)
        should_exit = self.kb.is_exit_command(clean_input)
        response = self._generate_response(clean_input)
        if should_exit:
            logger.info('Exit command received: %r', clean_input)
        return (response, should_exit)

    def _generate_response(self, clean_input: str) -> str:
        responses = self.kb.get_responses(clean_input)
        if responses is None:
            logger.debug('No rule matched for input: %r', clean_input)
            return self.kb.default_response
        reply = random.choice(responses)
        if reply == DYNAMIC_TIME_MARKER:
            return self._get_current_time_response()
        return reply

    @staticmethod
    def _get_current_time_response() -> str:
        current_time = datetime.now().strftime('%I:%M %p')
        return f'The current time is {current_time}.'
