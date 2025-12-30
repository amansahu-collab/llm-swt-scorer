from pydantic import BaseModel, Field
from typing import Literal


class EvaluateRequest(BaseModel):
    passage: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)


class EvaluateResponse(BaseModel):
    content_percentage: int | None = Field(
        None,
        ge=0,
        le=100,
        description="Content score as percentage (0–100)"
    )
    relevance_level: Literal["off-topic", "generic", "partial", "strong"]
    covered_ideas: list[str]
    missing_ideas: list[str]
    feedback: str = Field(..., max_length=100)
