"""Validated public contracts. Never place secrets in API response models."""

from pydantic import BaseModel, ConfigDict, Field


class Question(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(min_length=1)
    text: str = Field(min_length=1, max_length=1000)
    hint: str = Field(max_length=500)


class Pack(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(min_length=1)
    title: str = Field(min_length=1, max_length=120)
    role: str = Field(min_length=1, max_length=120)
    tags: list[str]
    description: str = Field(max_length=500)
    questions: list[Question] = Field(min_length=1)
