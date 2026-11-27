"""Single source of truth for tool input schemas."""
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

PackId = Annotated[Literal["frontend", "support", "graduate"], Field(description="Public starter pack to read")]
QuestionLimit = Annotated[int, Field(strict=True, ge=1, le=4, description="Maximum questions to return, from 1 to 4")]


class GetPackQuestions(BaseModel):
    """Read up to four questions and hints from a public InterviewCoach starter pack. Changes nothing."""

    model_config = ConfigDict(extra="forbid", strict=True)
    pack_id: PackId
    limit: QuestionLimit = 4
