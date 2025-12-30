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
    covered_ideas: list[str]
    missing_ideas: list[str]
    feedback: str
