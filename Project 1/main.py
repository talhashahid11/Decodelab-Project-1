from __future__ import annotations
import argparse
import logging
import sys
from pathlib import Path
from chatbot.bot import ChatBot
from chatbot.exceptions import KnowledgeBaseError
from chatbot.knowledge_base import KnowledgeBase
from chatbot.logging_config import configure_logging
logger = logging.getLogger('decodebot.main')
BANNER = "=======================================================\n DecodeBot - Rule-Based AI Chatbot (Project 1)\n Type 'exit' anytime to end the conversation.\n======================================================="

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='DecodeBot rule-based chatbot')
    parser.add_argument('--kb', default=str(Path(__file__).parent / 'data' / 'knowledge_base.json'), help='Path to the knowledge base JSON file (default: data/knowledge_base.json)')
    parser.add_argument('--debug', action='store_true', help='Enable verbose debug logging to the console')
    return parser.parse_args()

def run_repl(bot: ChatBot) -> None:
    print(BANNER)
    while True:
        try:
            raw_input_text = input('You: ')
        except (EOFError, KeyboardInterrupt):
            print('\nDecodeBot: Session interrupted. Goodbye!')
            break
        response, should_exit = bot.respond(raw_input_text)
        print(f'{bot.name}: {response}')
        if should_exit:
            break

def main() -> int:
    args = parse_args()
    configure_logging(debug=args.debug)
    try:
        knowledge_base = KnowledgeBase(args.kb)
    except KnowledgeBaseError as exc:
        logger.error('Failed to start DecodeBot: %s', exc)
        print(f'Error: {exc}', file=sys.stderr)
        return 1
    bot = ChatBot(knowledge_base=knowledge_base)
    run_repl(bot)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
