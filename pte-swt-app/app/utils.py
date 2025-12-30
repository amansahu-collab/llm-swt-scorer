# app/utils.py

import hashlib


def normalize_text(text: str) -> str:
    """
    Normalize text to reduce accidental variation.
    Keeps meaning intact.
    """
    return " ".join(text.strip().split())


def input_hash(passage: str, summary: str) -> str:
    """
    Stable hash for same passage + summary.
    Useful for determinism & future caching.
    """
    normalized = normalize_text(passage) + "||" + normalize_text(summary)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
