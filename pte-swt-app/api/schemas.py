from pydantic import BaseModel


class EvaluateRequest(BaseModel):
    passage: str
    summary: str


class EvaluateResponse(BaseModel):
    content_score: int | None
    relevance_level: str
    covered_ideas: list[str]
    missing_ideas: list[str]
    feedback: str
