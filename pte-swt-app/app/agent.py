# app/agent.py

import json
from groq import Groq
from typing import Dict, Any

from app.prompt import SYSTEM_PROMPT, build_user_prompt
from app.config import REQUEST_TIMEOUT

import os


class SWTAgent:
    """
    Deterministic AI agent for PTE SWT content scoring
    """

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")

        self.client = Groq(api_key=api_key)

        # LOCKED model config for determinism
        self.model_name = "llama-3.1-8b-instant"
        self.temperature = 0
        self.top_p = 1

    def evaluate(self, passage: str, summary: str) -> Dict[str, Any]:
        """
        Evaluate passage + summary and return STRICT JSON output
        """

        user_prompt = build_user_prompt(passage, summary)

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                temperature=self.temperature,
                top_p=self.top_p,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                timeout=REQUEST_TIMEOUT,
            )

            raw_output = response.choices[0].message.content.strip()

            # ---- STRICT JSON PARSING ----
            parsed = json.loads(raw_output)

            # ---- BASIC SAFETY CHECK ----
            required_keys = {
                "content_score",
                "relevance_level",
                "covered_ideas",
                "missing_ideas",
                "feedback",
            }

            if not required_keys.issubset(parsed.keys()):
                raise ValueError("Missing required keys in LLM output")

            return parsed

        except json.JSONDecodeError:
            return {
                "content_score": None,
                "relevance_level": "error",
                "covered_ideas": [],
                "missing_ideas": [],
                "feedback": "Model returned invalid JSON. Try again.",
            }

        except Exception as e:
            return {
                "content_score": None,
                "relevance_level": "error",
                "covered_ideas": [],
                "missing_ideas": [],
                "feedback": f"Evaluation failed: {str(e)}",
            }
