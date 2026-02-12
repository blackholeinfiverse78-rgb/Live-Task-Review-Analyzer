"""
FEATURE FREEZE COMPLETE - DEMO-ONLY MODE
Locked on: 2026-02-02
"""
import streamlit as st
import requests
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()

BACKEND_BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
if BACKEND_BASE_URL and not BACKEND_BASE_URL.startswith("http"):
    BACKEND_BASE_URL = f"http://{BACKEND_BASE_URL}"
BACKEND_URL = f"{BACKEND_BASE_URL.rstrip('/')}/api/v1/task"

TIMEOUT = 10  # Seconds
MAX_RETRIES = 3

def safe_post(url, json_data):
    """Robust POST with retries for demo network variability"""
    for attempt in range(MAX_RETRIES):
        try:
            res = requests.post(url, json=json_data, timeout=TIMEOUT)
            return res
        except requests.exceptions.RequestException as e:
            if attempt == MAX_RETRIES - 1:
                raise e
            time.sleep(1) # Wait before retry
    return None

st.set_page_config(
    page_title="Task Review AI (PROD)",
    page_icon="🛡️",
    layout="centered"
)

# Immutable Demo Data
DEMO_DATA = {
    "Live Editor": {"title": "", "desc": "", "demo": False, "type": None},
    "Good Submission": {
        "title": "Build a Secure Async API Gateway for User Authentication and Management",
        "desc": "The objective is to implement a robust API gateway. Requirements include schema validation using Pydantic, security constraints for JWT, and async database connections. This task ensures production readiness by adding caching and frontend integration layers. Final success criteria: 100% test coverage and full documentation.",
        "demo": True, "type": "good"
    },
    "Partial Submission": {
        "title": "Standardized Implementation of a basic API to handle standardized requests",
        "desc": "The Requirement is to make it work. The objective is to handle some requests. It should connect to a database eventually. Basic security constraints apply.",
        "demo": True, "type": "partial"
    },
    "Poor Submission": {
        "title": "Fix bug",
        "desc": "fix the bugs in the code quickly",
        "demo": True, "type": "poor"
    }
}

st.title("🛡️ Task Review AI")

# Locked Scenario Selection
scenario = st.selectbox("Select Scenario", options=list(DEMO_DATA.keys()))
current = DEMO_DATA[scenario]

with st.form("main_form"):
    t_title = st.text_input("Task Title", value=current["title"], disabled=current["demo"])
    t_desc = st.text_area("Task Description", value=current["desc"], disabled=current["demo"], height=200)
    submitted_by = st.text_input("Name", value="Demo Professional")
    run_btn = st.form_submit_button("Analyze Submission", type="primary")

if run_btn:
    if not t_title.strip() or not t_desc.strip():
        st.error("Validation Failure: Both title and description are strictly required.")
    else:
        try:
            # Phase 1: Storage
            with st.spinner("Processing..."):
                res = safe_post(f"{BACKEND_URL}/submit", {
                    "task_title": t_title, "task_description": t_desc,
                    "submitted_by": submitted_by, "is_demo": current["demo"],
                    "demo_type": current["type"]
                })
                
                if res.status_code == 422:
                    review = res.json()
                    # Mock a "Next Task" for failures
                    next_t = {
                        "next_task_title": "Input Fix Required",
                        "rationale": "Validation thresholds not met."
                    }
                elif res.status_code != 200:
                    st.error(f"System Error: {res.text}")
                    st.stop()
                else:
                    tid = res.json()["task_id"]
                    # Phase 2: Analysis
                    res = safe_post(f"{BACKEND_URL}/review", {"task_id": tid})
                    res.raise_for_status()
                    review = res.json()

                    # Phase 3: Transition
                    res = safe_post(f"{BACKEND_URL}/generate-next", review)
                    res.raise_for_status()
                    next_t = res.json()
                
            # Render Premium UI
            st.divider()
            
            # Status Badge Header
            status_colors = {"pass": "green", "borderline": "orange", "fail": "red"}
            status_color = status_colors.get(review['status'], "blue")
            st.markdown(f"### Status: :{status_color}[{review['status'].upper()}]")

            c1, c2, c3 = st.columns(3)
            c1.metric("Score", f"{review['score']}/100")
            c2.metric("Readiness", f"{review['readiness_percent']}%")
            c3.metric("Eval Time", f"{review['meta']['evaluation_time_ms']}ms")
            
            # Analysis Radar/Metrics
            st.markdown("#### Technical Analysis")
            a1, a2, a3 = st.columns(3)
            a1.progress(review['analysis']['technical_quality'] / 100, text=f"Tech: {review['analysis']['technical_quality']}%")
            a2.progress(review['analysis']['clarity'] / 100, text=f"Clarity: {review['analysis']['clarity']}%")
            a3.progress(review['analysis']['discipline_signals'] / 100, text=f"Discipline: {review['analysis']['discipline_signals']}%")

            with st.expander("Failure Reasons & Gaps", expanded=True):
                if review['failure_reasons']:
                    for gap in review['failure_reasons']: 
                        st.markdown(f"❌ {gap}")
                else: 
                    st.success("No critical failure reasons detected.")

            with st.expander("Optimization Hints", expanded=True):
                if review['improvement_hints']:
                    for h in review['improvement_hints']: 
                        st.markdown(f"✨ {h}")
                else: 
                    st.write("Task quality meets all optimization thresholds.")
            
            st.info(f"**Recommended Next Step:** {next_t['next_task_title']}")
            st.caption(f"**Rationale:** {next_t['rationale']}")
            
            st.toast(f"Evaluation complete in {review['meta']['evaluation_time_ms']}ms using {review['meta']['mode']} mode.", icon="✅")
            
        except Exception as e:
            st.error(f"System Error: Analysis could not be completed. {str(e)}")

st.sidebar.markdown("**System: Production Locked**")
try:
    health_url = BACKEND_URL.replace("/api/v1/task", "/health")
    health = requests.get(health_url, timeout=1).json()
    st.sidebar.success(f"Backend v{health['version']}")
except:
    st.sidebar.error("Backend Offline")

st.sidebar.caption("Deterministic Engine v2.0")
