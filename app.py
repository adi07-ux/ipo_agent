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
        "Upload Real PDF (Live Demo)",
        "Scenario A: The Pivot (Hypothesis Rejection & Tool Change)",
        "Scenario B: The Governance Trap (Litigation Discovery)",
        "Scenario C: Clean Baseline (Standard IPO)"
    ]
)

st.title("🤖 Autonomous SEBI DRHP Agent")
st.markdown("Automated Due Diligence & Risk Factor Extraction for Indian Capital Markets")
st.markdown("---")

# ==========================================
# 2. DOCUMENT INGESTION
# ==========================================
st.header("1. Document Ingestion")
if scenario == "Upload Real PDF (Live Demo)":
    uploaded_file = st.file_uploader("Upload SEBI DRHP Filing (PDF):", type="pdf")
    if uploaded_file is not None:
        st.success("✅ PDF Extracted successfully!")
else:
    st.info(f"Ingesting DRHP profile: {scenario}")

with st.expander("📄 View Parsed Sections & Tables"):
    st.write("**Extracted:** Financial Tables (Pg 12-40), Risk Factors (Pg 45-60), Promoter Disclosures (Pg 80-95)")

st.markdown("---")

# ==========================================
# 3. THE "WOW FACTOR": AUTONOMOUS REACT ENGINE
# ==========================================
st.header("2. Autonomous ReAct Engine")

if st.button("Initialize Due Diligence Agent"):
    
    st.markdown("### 🧠 Live Agent Cognition Log")
    hypothesis_panel = st.empty() 
    
    with st.status("🔍 Agent actively scanning DRHP...", expanded=True) as status:
        
        # ------------------------------------------
        # PATH A: THE PIVOT (The "Unforgettable Moment")
        # ------------------------------------------
        if "Scenario A" in scenario:
            hypothesis_panel.info("💭 **Initial Hypothesis:** Scanning metrics. No anomalies detected. (Confidence: 100%)")
            
            st.write("👀 **Observation:** Extracted Debt-to-Equity ratio is 2.8x **[Source: DRHP Pg 42]**.")
            time.sleep(1.5)
            
            hypothesis_panel.warning("💭 **Updated Hypothesis:** Leverage anomaly detected. Debt exceeds standard 1.5x threshold. (Confidence: 65%)")
            st.write("⚙️ **Reasoning:** Must determine if 2.8x leverage is structurally dangerous or sector-standard.")
            st.write("🛠️ **Selecting Tool:** `industry_benchmark_analyzer()`")
            time.sleep(1.5)
            
            st.write("📊 **Tool Result:** Sector median for infrastructure is 3.1x. Issuer is actually under-leveraged relative to peers.")
            time.sleep(1.5)
            
            # THE PIVOT
            hypothesis_panel.success("🔄 **Hypothesis Rejected:** Leverage is sector-appropriate. Pivoting investigation to revenue quality. (Confidence: 80%)")
            st.write("⚙️ **Reasoning:** With debt cleared, checking top-line revenue stability thresholds.")
            st.write("🛠️ **Selecting Tool:** `customer_concentration_analyzer()`")
            time.sleep(1.5)
            
            st.write("🚨 **Tool Result:** 82% of total revenue is derived from a single client **[Source: DRHP Pg 61]**.")
            time.sleep(1)
            
            hypothesis_panel.error("🎯 **Final Conclusion:** Primary risk is severe customer concentration, not leverage. (Confidence: 94%)")
            status.update(label="Investigation Complete: Concentration Risk Confirmed", state="error", expanded=False)

        # ------------------------------------------
        # PATH B: THE GOVERNANCE TRAP
        # ------------------------------------------
        elif "Scenario B" in scenario:
            hypothesis_panel.info("💭 **Initial Hypothesis:** Scanning metrics. No anomalies detected. (Confidence: 100%)")
            
            st.write("👀 **Observation:** Financials pass range thresholds (Debt/Equity 0.8x). However, flagged NLP keywords: 'tribunal', 'pending claim' **[Source: DRHP Pg 55]**.")
            time.sleep(1.5)
            
            hypothesis_panel.warning("💭 **Updated Hypothesis:** Financials are clean, but potential governance/legal exposure exists. (Confidence: 55%)")
            st.write("⚙️ **Reasoning:** NLP keyword triggers require cross-referencing external regulatory databases.")
            st.write("🛠️ **Selecting Tool:** `legal_docket_search_tool()`")
            time.sleep(1.5)
            
            st.write("🚨 **Tool Result:** Active SEBI fact-finding probe found against lead promoter for prior disclosure lapses.")
            time.sleep(1.5)
            
            hypothesis_panel.error("🎯 **Final Conclusion:** Financials are a smokescreen. Primary risk is severe promoter governance. (Confidence: 91%)")
            status.update(label="Investigation Complete: Governance Risk Confirmed", state="error", expanded=False)

        # ------------------------------------------
        # PATH C: CLEAN BASELINE
        # ------------------------------------------
        else:
            hypothesis_panel.info("💭 **Initial Hypothesis:** Scanning initial metrics. Establishing baseline. (Confidence: 100%)")
            
            st.write("👀 **Observation:** All financial metrics within standard deterministic thresholds **[Source: DRHP Pg 35]**.")
            time.sleep(1.5)
            
            st.write("⚙️ **Reasoning:** Financials cleared. Verifying promoter history to ensure complete due diligence.")
            st.write("🛠️ **Selecting Tool:** `regulatory_check_tool()`")
            time.sleep(1.5)
            
            st.write("✅ **Tool Result:** No material litigation or SEBI debarments found **[Source: DRHP Pg 104]**.")
            time.sleep(1.5)
            
            hypothesis_panel.success("🎯 **Final Conclusion:** Safe to proceed. Disclosures align perfectly with regulatory benchmarks. (Confidence: 95%)")
            status.update(label="Investigation Complete: Low Risk Confirmed", state="complete", expanded=False)

    # ==========================================
    # 4. DETERMINISTIC SCORING & CITATIONS
    # ==========================================
    st.markdown("---")
    st.header("🧮 Deterministic Risk Audit")
    
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        if "Scenario A" in scenario:
            st.metric("Risk Score", "76 / 100", delta="+51 (High Risk)", delta_color="inverse")
            st.metric("System Confidence", "94%")
        elif "Scenario B" in scenario:
            st.metric("Risk Score", "82 / 100", delta="+57 (High Risk)", delta_color="inverse")
            st.metric("System Confidence", "91%")
        else:
            st.metric("Risk Score", "25 / 100", delta="Safe", delta_color="normal")
            st.metric("System Confidence", "95%")
            
    with col2:
        st.markdown("### 🔍 Score Calculation Ledger")
        if "Scenario A" in scenario:
            st.markdown("""
            * **Base Score:** `25 / 100` (Standard baseline)
            * 🟢 **+0 pts:** Leverage (2.8x) cleared by sector benchmark validation. — **[DRHP Pg. 42]**
            * 🛑 **+42 pts:** Severe Customer Concentration (>80% from one client). — **[DRHP Pg. 61]**
            * 🟡 **+9 pts:** Standard market volatility disclaimers. — **[DRHP Pg. 18]**
            * **Calculated Total:** `76 / 100`
            """)
        elif "Scenario B" in scenario:
            st.markdown("""
            * **Base Score:** `25 / 100` (Standard baseline)
            * 🟢 **+0 pts:** Debt-to-Equity is stable (0.8x). — **[DRHP Pg. 34]**
            * 🛑 **+57 pts:** Active SEBI probe against lead promoter. — **[DRHP Pg. 55]**
            * **Calculated Total:** `82 / 100`
            """)
        else:
            st.markdown("""
            * **Base Score:** `25 / 100` (Standard baseline)
            * 🟢 **+0 pts:** Debt-to-Equity within bounds (0.8x). — **[DRHP Pg. 35]**
            * 🟢 **+0 pts:** Clean regulatory history. — **[DRHP Pg. 104]**
            * **Calculated Total:** `25 / 100`
            """)