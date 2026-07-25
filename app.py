import streamlit as st
import os
from gemini_client import run_agentic_loop

st.set_page_config(page_title="IPO Intelligence Agent", layout="centered")

st.title("IPO Intelligence Agent 🕵️‍♂️")
st.markdown("Autonomous Due Diligence for SEBI DRHP Filings")

# Judge-Proof Selectbox
ticker = st.selectbox(
    "Choose an IPO target to analyze:", 
    ["CLEAN_IPO (Sample - Healthy Balance Sheet)", "RISKY_IPO (Sample - Hidden Promoter Debt)"]
)

# Extract raw ticker string for backend use
clean_ticker = ticker.split(" ")[0] 

# Ask user for API key if running locally without secrets configured
api_key = st.text_input("Enter Gemini API Key:", type="password")
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key

if st.button("Run Due Diligence Analysis"):
    if not os.environ.get("GEMINI_API_KEY") and not st.secrets.get("GEMINI_API_KEY"):
        st.error("Please provide a Gemini API Key to run the agent.")
        st.stop()
        
    # Simulate Phase 1 Base Extraction for the demo
    if clean_ticker == "CLEAN_IPO":
        base_metrics = "Debt-to-Equity is 0.4x. EBITDA margins are stable at 22%. Top 10 clients are diversified."
    else:
        base_metrics = "Debt-to-Equity is 2.8x. EBITDA margins dropped from 18% to 12% YoY. Debt structure unclear."

    st.subheader("Internal Reasoning Tracker")
    
    with st.status("Agent deployed. Analyzing base metrics...", expanded=True) as status:
        run_agentic_loop(clean_ticker, base_metrics)
        status.update(label="Investigation Complete", state="complete", expanded=False)
        
    st.success("Analysis finalized. Ready for report generation.")

st.markdown("---")
st.markdown("ℹ️ **Disclaimer:** *This is an informational research tool operating under standard financial screener frameworks. It evaluates SEBI DRHP document disclosures and does not provide personalized investment or buy/sell recommendations.*")