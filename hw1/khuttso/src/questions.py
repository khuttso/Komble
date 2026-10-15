"""Input and output contracts for the individual question-generator feature."""

import json
from pathlib import Path

from llm import CoachError


LEVELS = ("intern", "junior", "mid-level")


def validate_input(role: str, level: str) -> tuple[str, str]:
    role = role.strip()
    level = level.strip().casefold()
    if not 1 <= len(role) <= 100:
        raise CoachError("Enter a job role between 1 and 100 characters after trimming.")
    if level not in LEVELS:
        raise CoachError("Level must be intern, junior, or mid-level.")
    return role, level


def build_messages(role: str, level: str) -> list[dict[str, str]]:
    prompt = Path(__file__).with_name("questions.txt").read_text(encoding="utf-8")
    return [
        {"role": "system", "content": prompt},
        {"role": "user", "content": json.dumps({"role": role, "level": level})},
    ]


def validate_questions(value: object) -> list[dict[str, str]]:
    """Reject unusable output; never repair or partially display model responses."""
    message = "The model returned invalid questions. Try again manually."
    if not isinstance(value, dict) or set(value) != {"questions"}:
        raise CoachError(message)
    items = value["questions"]
    if not isinstance(items, list) or len(items) != 3:
        raise CoachError(message)
    result = []
    seen = set()
    for item in items:
        if not isinstance(item, dict) or set(item) != {"question", "assesses"}:
            raise CoachError(message)
        question, assesses = item["question"], item["assesses"]
        if not isinstance(question, str) or not isinstance(assesses, str):
            raise CoachError(message)
        question, assesses = question.strip(), assesses.strip()
        if (
            not 1 <= len(question) <= 500
            or not question.endswith("?")
            or not 1 <= len(assesses) <= 300
            or question.casefold() in seen
        ):
            raise CoachError(message)
        seen.add(question.casefold())
        result.append({"question": question, "assesses": assesses})
    return result
