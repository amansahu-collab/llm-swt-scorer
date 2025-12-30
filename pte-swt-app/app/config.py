# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# N8N WEBHOOK
# -----------------------------
N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "https://n8n.srv1102521.hstgr.cloud/webhook/ea89d7d3-3f6c-49f5-80fc-b5fd4be94dd0"
)

# -----------------------------
# UI SETTINGS
# -----------------------------
APP_TITLE = "PTE SWT Content Scorer"
PASSAGE_LABEL = "Passage (Paragraph)"
SUMMARY_LABEL = "Student Summary (1 sentence)"

# -----------------------------
# TIMEOUT / RETRIES
# -----------------------------
REQUEST_TIMEOUT = 30  # seconds
