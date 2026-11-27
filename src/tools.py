"""Read the application's current catalogue, without a model, key or private data."""
from dataclasses import dataclass
from typing import Callable

from pydantic import BaseModel

from project.backend.app import content
from project.backend.app.schemas import Question
from .contracts import GetPackQuestions


class ToolFailure(Exception):
    """Safe expected failure whose message tells the caller what to do next."""


class PackQuestions(BaseModel):
    pack_id: str
    title: str
    questions: list[Question]
    returned: int
    total: int


def get_pack_questions(args: GetPackQuestions) -> PackQuestions:
    pack = next((pack for pack in content.PACKS if pack.id == args.pack_id), None)
    if pack is None:
        raise ToolFailure("This starter pack is unavailable. Choose another advertised pack or ask the maintainer to restore it.")
    questions = [question.model_copy(deep=True) for question in pack.questions[:args.limit]]
    return PackQuestions(pack_id=pack.id, title=pack.title, questions=questions,
                         returned=len(questions), total=len(pack.questions))


@dataclass(frozen=True)
class Tool:
    args: type[BaseModel]
    run: Callable

    def schema(self, name: str) -> dict:
        return {"type": "function", "function": {"name": name,
                "description": self.args.__doc__.strip(),
                "parameters": self.args.model_json_schema()}}


TOOLS = {"get_pack_questions": Tool(GetPackQuestions, get_pack_questions)}


def tools_for(caller: str | None = None) -> dict[str, Tool]:
    """Only public read tools exist; visitors and signed-in callers get the same access.

    caller is trusted host context, never an input to a tool or a logged identity.
    """
    return dict(TOOLS)
