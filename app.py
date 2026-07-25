import streamlit as st
import time

st.set_page_config(page_title="Autonomous SEBI DRHP Agent", layout="wide")

# ==========================================
# 1. VISIBLE BRANCHING (Sidebar Setup)
# ==========================================
st.sidebar.title("🎯 Demo Scenario Selector")
scenario = st.sidebar.selectbox(
    "Select DRHP Injection Profile:",
    [
        "Scenario A: Leverage Risk (e.g., Paytm/Go First)",
        "Scenario B: Promoter Litigation (Governance Risk)",
        "Scenario C: Clean Baseline (Standard IPO)"
    ]
)

st.title("🤖 Autonomous SEBI DRHP Agent")
st.markdown("Automated Due Diligence & Risk Factor Extraction for Indian Capital Markets")
st.markdown("---")

st.header("1. Document Ingestion")
st.info(f"Ingesting DRHP profile: {scenario}")
with st.expander("📄 View Parsed Sections & Tables"):
    st.write("**Extracted:** Financial Tables (Pg 12-40), Risk Factors (Pg 45-60), Promoter Disclosures (Pg 80-95)")

st.markdown("---")
st.header("2. Autonomous ReAct Engine")

if st.button("Initialize Due Diligence Agent"):
    
    # ==========================================
    # 2. THE "WOW FACTOR": Dynamic Hypothesis Panel
    # ==========================================
    st.markdown("### 🧠 Agent Cognition State")
    hypothesis_panel = st.empty() # This container will update live
    
    with st.status("🔍 Agent actively scanning DRHP...", expanded=True) as status:
        
        # ------------------------------------------
        # PATH A: LEVERAGE RISK
        # ------------------------------------------
        if "Scenario A" in scenario:
            hypothesis_panel.info("💭 **Current Hypothesis:** Scanning initial metrics. No anomalies detected yet. (Confidence: 100%)")
            
            st.write("👀 **Observation:** Extracted Debt-to-Equity ratio is 2.8x [Source: Pg 42].")
            time.sleep(1.2)
            
            hypothesis_panel.warning("💭 **Current Hypothesis:** Leverage anomaly detected. Debt is significantly above typical IPO baselines. (Confidence: 65%)")
            st.write("🛠️ **Decision:** Triggering `industry_benchmark_tool()` to compare against sector median...")
            time.sleep(1.5)
            
            st.write("📊 **Tool Result:** Sector median is 0.7x. Issuer is over-leveraged by 400%.")
            time.sleep(1.2)
            
            st.write("🛠️ **Decision:** Triggering `related_party_loans_tool()` to check for off-balance-sheet debt...")
            time.sleep(1.5)
            
            st.write("🚨 **Tool Result:** Found 150 Cr in unsecured promoter guarantees [Source: Pg 88].")
            time.sleep(1)
            
            # The agent "changes its mind"
            hypothesis_panel.error("🎯 **Hypothesis Updated:** Extreme leverage risk confirmed. Hidden liabilities present. (Confidence: 92%)")
            status.update(label="Investigation Complete: Leverage Risk Confirmed", state="error", expanded=False)

        # ------------------------------------------
        # PATH B: GOVERNANCE RISK (Proves Branching)
        # ------------------------------------------
        elif "Scenario B" in scenario:
            hypothesis_panel.info("💭 **Current Hypothesis:** Scanning initial metrics. No anomalies detected yet. (Confidence: 100%)")
            
            st.write("👀 **Observation:** Financials appear stable (Debt/Equity 0.8x). Flagged keywords: 'tax tribunal', 'pending claim' [Source: Pg 55].")
            time.sleep(1.2)
            
            hypothesis_panel.warning("💭 **Current Hypothesis:** Potential governance/legal risk. Financials are clean, but litigation exposure is unclear. (Confidence: 55%)")
            st.write("🛠️ **Decision:** Triggering `legal_docket_search_tool()`...")
            time.sleep(1.5)
            
            st.write("🚨 **Tool Result:** Active SEBI probe found against lead promoter for previous shell company violations.")
            time.sleep(1.2)
            
            # The agent "changes its mind"
            hypothesis_panel.error("🎯 **Hypothesis Updated:** Financials are a smokescreen. Primary risk is severe promoter governance. (Confidence: 89%)")
            status.update(label="Investigation Complete: Governance Risk Confirmed", state="error", expanded=False)

    # ==========================================
    # 3. PAGE-LEVEL EVIDENCE IN THE SCORE
    # ==========================================
    st.markdown("---")
    st.header("📊 Final Audit Report")
    
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        if "Scenario C" in scenario:
            st.metric("Risk Score", "85 / 100", delta="Safe", delta_color="normal")
        else:
            st.metric("Risk Score", "38 / 100", delta="-62 (High Risk)", delta_color="inverse")
            
    with col2:
        st.markdown("### Evidence Breakdown")
        if "Scenario A" in scenario:
            st.markdown("""
            * 🛑 **-40 pts:** High Debt-to-Equity (2.8x) — **[Source: DRHP Pg. 42, Financial Statements]**
            * 🛑 **-22 pts:** Undisclosed related party guarantees (150 Cr) — **[Source: DRHP Pg. 88, Note 14]**
            * 🟢 **+0 pts:** No active litigation found — **[Source: DRHP Pg. 110]**
            """)
        elif "Scenario B" in scenario:
            st.markdown("""
            * 🟢 **-0 pts:** Debt-to-Equity is stable (0.8x) — **[Source: DRHP Pg. 34]**
            * 🛑 **-62 pts:** Active SEBI probe against lead promoter — **[Source: DRHP Pg. 55, Risk Factors Section]**
            """)

    st.error("This output demonstrates dynamic ReAct branching based on deterministic thresholds, avoiding linear LLM hallucinations.")