import streamlit as st
import os
import pdfplumber
from gemini_client import execute_agentic_loop

st.set_page_config(page_title="IPO Due Diligence Agent", page_icon="📈", layout="wide")
st.title("📈 Autonomous SEBI DRHP Agent")

# Sidebar configurations
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key

st.sidebar.markdown("### Test Architecture")
test_target = st.sidebar.selectbox("Choose Target IPO:", [
    "CLEAN_IPO (Sample - Healthy Balance Sheet)",
    "RISKY_IPO (Sample - Hidden Promoter Debt)"
])

# Mock data mapping for live pitch reliability
mock_metrics = {
    "CLEAN_IPO (Sample - Healthy Balance Sheet)": "Debt-to-Equity is 0.4x. EBITDA margins stable at 22%. Top 10 clients account for 15% of revenue. No legal disputes found.",
    "RISKY_IPO (Sample - Hidden Promoter Debt)": "Debt-to-Equity is 2.8x. Unclear debt structure. EBITDA margin compression from 18% to 12% YoY."
}

# Phase 1: PDF Extraction logic
st.subheader("1. Extract Base Metrics")
uploaded_file = st.file_uploader("Upload SEBI DRHP Filing (PDF):", type="pdf")
drhp_data = ""

if uploaded_file:
    with st.spinner("Extracting text via pdfplumber..."):
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                # Extract first 5 pages for speed during demo
                pages = [page.extract_text() for page in pdf.pages[:5]]
                drhp_data = "\n".join(filter(None, pages))
            st.success("PDF Extracted successfully!")
            with st.expander("View Extracted Text"):
                st.text(drhp_data[:1500] + "...")
        except Exception as e:
            st.error(f"Error parsing PDF: {e}")
else:
    st.info(f"Using test case metrics for: {test_target}")
    drhp_data = mock_metrics[test_target]

# Phase 3: Run the end-to-end loop
st.subheader("2. ReAct Agent Engine")
if st.button("Run Due Diligence Analysis"):
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("Please provide your Gemini API key.")
    else:
        execute_agentic_loop(test_target.split()[0], drhp_data)

# Phase 4: Final UI Polish
st.divider()
st.caption("ℹ️ **Disclaimer:** *This is an informational research tool operating under standard financial screener frameworks. It evaluates SEBI DRHP document disclosures and does not provide personalized investment or buy/sell recommendations.*")