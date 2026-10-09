import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data_app import analyze_text
from src.data_profiles import PROFILES


def main():
    st.set_page_config(page_title="ResumeLens", layout="wide")
    st.title("ResumeLens")
    st.caption("ML Engineer and Data Architect: qualification patterns, not a hiring ranking.")
    example = (ROOT / "examples/data_profiles/ml_and_architect.txt").read_text(encoding="utf-8")
    text = st.text_area("Résumé text", value=example, height=260)
    uploaded = st.file_uploader("Or upload a UTF-8 .txt file (takes precedence)", type=["txt"])
    if uploaded is not None:
        try:
            text = uploaded.getvalue().decode("utf-8-sig")
        except UnicodeDecodeError:
            st.error("Use a UTF-8 text file.")
            return
    profile = st.selectbox("Profiles", ["all", *PROFILES],
                           format_func=lambda key: "Both available profiles" if key == "all" else PROFILES[key]["label"])
    if st.button("Analyze", key="analyze"):
        try:
            st.session_state["analysis"] = (text, profile, *analyze_text(text, profile))
        except ValueError as error:
            st.session_state.pop("analysis", None)
            st.error(str(error))
    analysis = st.session_state.get("analysis")
    if analysis is None:
        return
    old_text, old_profile, report, documents = analysis
    if (text, profile) != (old_text, old_profile):
        st.info("Inputs changed. Analyze again to obtain current results.")
        return
    for result in report["profiles"].values():
        with st.expander(result["profile"], expanded=True):
            st.write("Pattern: " + ("ACCEPTED" if result["accepted"] else "REJECTED"))
            if result["missing_categories"]:
                st.write("Missing categories: " + ", ".join(result["missing_categories"]))
            raw, canonical, trace = st.tabs(["1. Extraction", "2. Normalization", "3. DFA trace"])
            with raw:
                st.json(result["extracted"])
            with canonical:
                st.write(result["qualifications"])
            with trace:
                st.dataframe(result["trace"], hide_index=True)
    st.subheader("4. DSL validation and visualization")
    st.write("Candidate export: " + report["export_status"])
    if "export_error" in report:
        st.warning(report["export_error"])
    st.download_button("Download report", json.dumps(report, ensure_ascii=False, indent=2),
                       "report.json", "application/json")
    if documents:
        dsl, markdown = documents
        st.download_button("Download DSL", dsl, "candidate.resume", "text/plain")
        st.download_button("Download Markdown", markdown, "candidate.md", "text/markdown")
        with st.expander("Validated DSL"):
            st.code(dsl, language="text")
        st.markdown(markdown)


if __name__ == "__main__":
    main()
