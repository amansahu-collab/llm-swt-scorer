<<<<<<< HEAD
from pydantic import BaseModel, Field
from typing import Literal


class EvaluateRequest(BaseModel):
    passage: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)


class EvaluateResponse(BaseModel):
    content_percentage: int | None
    score: int | None = Field(
        None,
        ge=0,
        le=4,
        description="PTE content score (0–4)"
    )
    relevance_level: Literal["off-topic", "generic", "partial", "strong"]
=======
from pydantic import BaseModel


class EvaluateRequest(BaseModel):
    passage: str
    summary: str


class EvaluateResponse(BaseModel):
    content_score: int | None
    relevance_level: str
>>>>>>> fee07bf (added project files)
    covered_ideas: list[str]
    missing_ideas: list[str]
    feedback: str
