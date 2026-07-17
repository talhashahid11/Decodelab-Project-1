# DecodeBot — Rule-Based AI Chatbot (Enhanced Edition)

**Internship:** DecodeLabs — Artificial Intelligence Track (Batch 2026)
**Module:** Project 1 — The Logic Engine (Deterministic Guardrails)

## Overview

DecodeBot is a fully deterministic, rule-based chatbot built with a
production-style Python package structure. It simulates conversation through
explicit dictionary-driven logic (not machine learning), demonstrating the
"white box" architecture that underpins real-world AI guardrail systems
(e.g. NVIDIA NeMo, Llama Guard) — traceable, safe, and 100% explainable.

This is an **enhanced, professional version** of the original single-file
submission, restructured as an installable package with tests, logging,
config-driven data, and proper error handling.

## Architecture

```
Input → sanitize → lookup in KnowledgeBase → resolve response → Output
```

| Layer | File | Responsibility |
|---|---|---|
| Data | `data/knowledge_base.json` | All intents/responses — editable without touching code |
| Loading & validation | `chatbot/knowledge_base.py` | Parses & validates the JSON, raises clear errors |
| Sanitization | `chatbot/utils.py` | Normalizes user input (case, whitespace) |
| Core logic | `chatbot/bot.py` | `ChatBot` class — the O(1) dictionary lookup engine |
| Logging | `chatbot/logging_config.py` | Console + rotating file logs |
| Errors | `chatbot/exceptions.py` | Custom exception types for clean failure handling |
| Entry point | `main.py` | CLI with `argparse`, the continuous REPL loop |
| Tests | `tests/test_chatbot.py` | 18 unit tests covering all core behavior |

## Why This Is "More Professional" Than a Single Script

- **Separation of concerns** — data, logic, and presentation live in
  different files instead of one script.
- **Config-driven knowledge base** — add/edit responses by editing JSON,
  no code changes or redeployment needed.
- **Object-oriented design** — `ChatBot` and `KnowledgeBase` are reusable,
  testable classes instead of loose functions and globals.
- **Proper error handling** — custom exceptions (`KnowledgeBaseError`,
  `EmptyInputError`) instead of silent failures or crashes.
- **Logging, not `print` debugging** — timestamped logs to both console and
  `logs/decodebot.log`, with a `--debug` flag for verbose output.
- **Automated tests** — 18 unit tests using `pytest`, covering sanitization,
  knowledge base validation, and bot behavior (including edge cases like
  empty input and malformed JSON).
- **CLI interface** — `argparse`-based flags (`--kb`, `--debug`) instead of
  hardcoded paths.
- **Type hints & docstrings** throughout for readability and IDE support.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Run the chatbot
python3 main.py

# Run with verbose debug logging
python3 main.py --debug

# Point to a custom knowledge base file
python3 main.py --kb path/to/custom_kb.json
```

Example session:

```
You: hello
DecodeBot: Hi there! How can I help you today?
You: what can you do
DecodeBot: Right now I can chat using predefined rules. I can also tell you the time and a joke!
You: time
DecodeBot: The current time is 11:23 AM.
You: exit
DecodeBot: Goodbye! Session ended.
```

## Running Tests

```bash
python3 -m pytest tests/ -v
```

All 18 tests should pass, covering:
- Input sanitization (case, whitespace, empty/None input)
- Knowledge base loading & validation (missing file, invalid JSON, missing keys)
- Bot response logic (known/unknown intents, exit handling, dynamic responses)

## Project Structure

```
decodebot/
├── chatbot/
│   ├── __init__.py
│   ├── bot.py               # ChatBot core class
│   ├── knowledge_base.py    # KnowledgeBase loader/validator
│   ├── logging_config.py    # Logging setup
│   ├── exceptions.py        # Custom exceptions
│   └── utils.py             # Input sanitization
├── data/
│   └── knowledge_base.json  # All intents & responses
├── tests/
│   ├── __init__.py
│   └── test_chatbot.py      # 18 unit tests
├── logs/                    # Runtime logs (generated on first run)
├── main.py                  # CLI entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements Checklist (Original DecodeLabs Spec)

- [x] Input Loop — continuous `while` cycle (`main.py::run_repl`)
- [x] Sanitization — case & whitespace normalization (`chatbot/utils.py`)
- [x] Knowledge Base — dictionary/JSON with 12 intents (spec required 5+)
- [x] Fallback — default response via `KnowledgeBase.get_responses()`
- [x] Exit Strategy — clean break via `is_exit_command()`

## Possible Next Steps (Project 2 Preview)

Per the internship brief, Project 2 moves from **discrete exact-match
lookups** to **continuous semantic matching** — replacing dictionary keys
with vector embeddings so the bot can understand meaning, not just exact
phrasing.

## Author

DecodeLabs Intern — Batch 2026

## Contact

📞 +91 89330 06408 · ✉ decodelabs.tech@gmail.com · 🌐 www.decodelabs.tech
