from fastapi import FastAPI
from api.schemas import EvaluateRequest, EvaluateResponse

from app.agent import SWTAgent
from app.utils import normalize_text

app = FastAPI(
    title="PTE SWT Content Scoring API",
    version="1.0.0"
)

agent = SWTAgent()


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate_swt(payload: EvaluateRequest):
    passage = normalize_text(payload.passage)
    summary = normalize_text(payload.summary)
    return agent.evaluate(passage, summary)
