from __future__ import annotations
import logging
from pathlib import Path

def configure_logging(log_dir: str='logs', debug: bool=False) -> None:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = Path(log_dir) / 'decodebot.log'
    formatter = logging.Formatter(fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger = logging.getLogger('decodebot')
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
