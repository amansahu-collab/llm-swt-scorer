# app/agent.py

import json
import os
from typing import Dict, Any

from groq import Groq

from app.prompt import SYSTEM_PROMPT, build_user_prompt
from app.config import REQUEST_TIMEOUT


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

    def percentage_to_score(percent: int) -> int:
        if percent >= 76:
            return 4
        elif percent >= 51:
            return 3
        elif percent >= 26:
            return 2
        elif percent >= 1:
            return 1
        else:
            return 0

    def evaluate(self, passage: str, summary: str) -> Dict[str, Any]:
        """
        Evaluate passage + summary and return STRICT JSON output
        """
    
        def percentage_to_score(percent: int) -> int:
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
    
            # ---- REQUIRED KEYS CHECK ----
            required_keys = {
                "content_percentage",
                "relevance_level",
                "covered_ideas",
                "missing_ideas",
                "feedback",
            }
    
            if not required_keys.issubset(parsed.keys()):
                raise ValueError("Missing required keys in LLM output")
    
            # ---- TYPE & RANGE SAFETY ----
            if not isinstance(parsed["content_percentage"], int):
                raise ValueError("content_percentage must be int")
    
            if not (0 <= parsed["content_percentage"] <= 100):
                raise ValueError("content_percentage out of range")
    
            # ---- DERIVED PTE SCORE (0–4) ----
            parsed["score"] = percentage_to_score(parsed["content_percentage"])
            # ---- FIX FEEDBACK FOR PERFECT SCORE ----
            if parsed["score"] == 4:
                parsed["feedback"] = "Excellent summary. The main idea and key outcomes are clearly conveyed."
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
    