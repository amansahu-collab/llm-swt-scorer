<<<<<<< HEAD
from app.agent import SWTAgent
from app.utils import input_hash, normalize_text
from app.config import (
=======
from agent import SWTAgent
from utils import input_hash, normalize_text
from config import (
>>>>>>> fee07bf (added project files)
    APP_TITLE,
    PASSAGE_LABEL,
    SUMMARY_LABEL,
)
import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title=APP_TITLE, layout="centered")
st.title(APP_TITLE)

st.caption("PTE Summarize Written Text – Content Scoring Only")

# -----------------------------
# SESSION STATE (determinism)
# -----------------------------
if "last_hash" not in st.session_state:
    st.session_state.last_hash = None
    st.session_state.last_result = None

# -----------------------------
# INPUTS
# -----------------------------
passage = st.text_area(PASSAGE_LABEL, height=220)
summary = st.text_area(SUMMARY_LABEL, height=100)

# -----------------------------
# EVALUATE BUTTON
# -----------------------------
if st.button("Evaluate"):
    if not passage.strip() or not summary.strip():
        st.warning("Passage aur Summary dono required hai.")
    else:
        norm_passage = normalize_text(passage)
        norm_summary = normalize_text(summary)
        current_hash = input_hash(norm_passage, norm_summary)

        # SAME INPUT → SAME OUTPUT (session-level)
        if current_hash == st.session_state.last_hash:
            result = st.session_state.last_result
        else:
            with st.spinner("Evaluating content..."):
                agent = SWTAgent()
                result = agent.evaluate(norm_passage, norm_summary)

                st.session_state.last_hash = current_hash
                st.session_state.last_result = result

        # -----------------------------
        # OUTPUT
        # -----------------------------
<<<<<<< HEAD
        if result.get("score") is None:
            st.error(result["feedback"])
        else:
            st.subheader("Result")

            # ---- MAIN SCORE (PTE STYLE) ----
            st.metric(
                "Content Score (0–4)",
                result["score"],
                help="Derived from content match percentage (PTE-style scoring)",
            )

            # ---- OPTIONAL DEBUG INFO (can remove later) ----
            st.caption(f'Raw content match: {result["content_percentage"]}%')
=======
        if result["content_score"] is None:
            st.error(result["feedback"])
        else:
            st.subheader("Result")
            st.metric("Content Score", result["content_score"], help="Scored strictly on key idea coverage, not relevance alone")
>>>>>>> fee07bf (added project files)

            st.write("**Relevance Level:**", result["relevance_level"])
            st.write("**Covered Ideas:**", ", ".join(result["covered_ideas"]) or "—")
            st.write("**Missing Ideas:**", ", ".join(result["missing_ideas"]) or "—")

            st.info(result["feedback"])
<<<<<<< HEAD

            if result["score"] <= 1:
                st.warning(
                    "Tip: Clearly state the main idea and outcome, not just the topic."
                )
=======
            if result["content_score"] <= 1:
                st.warning("Tip: Mention the main purpose or outcome of the passage, not just a generic topic.")

# -----------------------------
>>>>>>> fee07bf (added project files)
