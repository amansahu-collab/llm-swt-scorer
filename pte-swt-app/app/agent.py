# app/agent.py

import json
from typing import Dict, Any

from app.llm_client import LocalLLMClient
from app.prompt import SYSTEM_PROMPT, build_user_prompt


class SWTAgent:
    """
    Deterministic AI agent for PTE SWT content scoring
    (Local LLM via Ollama)
    """

    def __init__(self):
        # ✅ REAL local LLM (Ollama)
        self.llm = LocalLLMClient()
        self.model_name = "llama3.1:8b"  # informational, used by Ollama

    def percentage_to_score(self, percent: int) -> int:
        if percent >= 76:
            return 4
        elif percent >= 51:
            return 3
        elif percent >= 26:
            return 2
        elif percent >= 5:
            return 1
        else:
            return 0

    def evaluate(self, passage: str, summary: str) -> Dict[str, Any]:
        """
        Evaluate passage + summary and return STRICT JSON output
        """

        word_count = len(summary.split())

        # ---- HARD RULE: TOO SHORT ----
        if word_count < 14:
            return {
                "content_percentage": 0,
                "score": 0,
                "relevance_level": "off-topic",
                "covered_ideas": [],
                "missing_ideas": ["main idea", "purpose or outcome"],
                "feedback": "Too short to show understanding. Use 14+ words.",
            }

        user_prompt = build_user_prompt(passage, summary)

        try:
            # ✅ LOCAL LLM CALL (OLLAMA)
            raw_output = self.llm.chat(SYSTEM_PROMPT, user_prompt)

            # ---- STRICT JSON PARSING ----
            parsed = json.loads(raw_output)

            required_keys = {
                "content_percentage",
                "relevance_level",
                "covered_ideas",
                "missing_ideas",
                "feedback",
            }

            if not required_keys.issubset(parsed.keys()):
                raise ValueError("Missing required keys in LLM output")

            if not isinstance(parsed["content_percentage"], int):
                raise ValueError("content_percentage must be int")

            if not (0 <= parsed["content_percentage"] <= 100):
                raise ValueError("content_percentage out of range")

            # ---- DERIVED SCORE (0–4) ----
            parsed["score"] = self.percentage_to_score(
                parsed["content_percentage"]
            )

            # ---- PERFECT SCORE FIX ----
            if parsed["score"] == 4:
                parsed["feedback"] = (
                    "Excellent summary. The main idea and key outcomes are clearly conveyed."
                )
                parsed["missing_ideas"] = []

            return parsed

        except json.JSONDecodeError:
            return {
                "content_percentage": None,
                "score": None,
                "relevance_level": "off-topic",
                "covered_ideas": [],
                "missing_ideas": [],
                "feedback": "Invalid model output. Please retry.",
            }

        except Exception:
            return {
                "content_percentage": None,
                "score": None,
                "relevance_level": "off-topic",
                "covered_ideas": [],
                "missing_ideas": [],
                "feedback": "Evaluation failed. Please retry.",
            }
