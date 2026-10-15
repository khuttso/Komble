"""Run with: python hw1/khuttso/src/main.py --role developer --level junior"""

import argparse
import json
import os
import sys

from llm import CoachError, OpenRouterClient, Settings
from questions import build_messages, validate_input, validate_questions


DISCLOSURE = (
    "Your job role and experience level are sent to an external AI provider "
    "(OpenRouter and its model provider). Omit sensitive information. "
    "Generated questions are practice material, not actual employer questions."
)


def main(argv=None, *, environment=None, transport=None, stdout=None, stderr=None) -> int:
    stdout = stdout if stdout is not None else sys.stdout
    stderr = stderr if stderr is not None else sys.stderr
    parser = argparse.ArgumentParser(
        description="Generate three interview practice questions for a role and level.",
        epilog=DISCLOSURE,
    )
    parser.add_argument("--role", required=True, help="Job role, 1-100 trimmed characters.")
    parser.add_argument("--level", required=True, help="intern, junior, or mid-level (case-insensitive).")
    args = parser.parse_args(argv)
    try:
        role, level = validate_input(args.role, args.level)
        settings = Settings.from_environment(os.environ if environment is None else environment)
        messages = build_messages(role, level)
        print(DISCLOSURE, file=stderr)
        client = OpenRouterClient(settings, stderr, transport=transport)
        questions = client.complete_json(messages, validate_questions)
        print(json.dumps({"role": role, "level": level, "questions": questions}), file=stdout)
        return 0
    except CoachError as error:
        print(f"Error: {error}", file=stderr)
        return 1
    except OSError:
        print("Error: Could not read the local prompt or write the output.", file=stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
