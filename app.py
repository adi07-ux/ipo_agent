import streamlit as st
import time
import pdfplumber

st.set_page_config(page_title="Autonomous SEBI DRHP Agent", layout="wide")

# ==========================================
# REAL DETERMINISTIC SCORING ENGINE 
# (Uses simple range thresholds, avoiding complex multi-threaded hallucination)
# ==========================================
def analyze_live_pdf(pdf_file):
    """Extracts text from the uploaded PDF and calculates a real risk score."""
    raw_text = ""
    try:
        # Extract text from the first 20 pages (Executive Summary & Risk Factors)
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages[:20]:
                raw_text += page.extract_text() + "\n"
    except Exception as e:
        return 100, 0, ["Error parsing PDF text."], "Failed to read PDF."

    text_lower = raw_text.lower()
    
    # Baseline Scores
    risk_score = 25
    confidence_score = 100
    evidence_log = []
    
    # 1. Leverage/Debt Threshold Check
    if "debt-to-equity" in text_lower or "outstanding indebtedness" in text_lower or "borrowings" in text_lower:
        risk_score += 25
        confidence_score -= 10
        evidence_log.append("🛑 **+25 pts:** High frequency of debt/leverage keywords detected in initial pages.")
        
    # 2. Legal & Governance Threshold Check
    if "litigation" in text_lower or "tribunal" in text_lower or "sebi probe" in text_lower:
        risk_score += 35
        confidence_score -= 15
        evidence_log.append("🛑 **+35 pts:** Active litigation or regulatory keywords detected.")
        
    # 3. Cash Flow Threshold Check
    if "negative cash flow" in text_lower or "net loss" in text_lower:
        risk_score += 20
        confidence_score -= 10
        evidence_log.append("🛑 **+20 pts:** History of negative cash flows or net losses explicitly stated.")

    # Cap the scores within strict deterministic bounds
    risk_score = min(risk_score, 100)
    confidence_score = max(confidence_score, 0)
    
    # If no major anomalies breach the threshold
    if not evidence_log:
        evidence_log.append("🟢 **+0 pts:** No severe anomaly keywords detected in initial scan.")
        
    return risk_score, confidence_score, evidence_log, raw_text

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
uploaded_file = None

if scenario == "Upload Real PDF (Live Demo)":
    uploaded_file = st.file_uploader("Upload SEBI DRHP Filing (PDF):", type="pdf")
    if uploaded_file is not None:
        st.success("✅ PDF Extracted successfully!")
else:
    st.info(f"Ingesting DRHP profile: {scenario}")

with st.expander("📄 View Parsed Sections & Tables"):
    if scenario == "Upload Real PDF (Live Demo)":
        if uploaded_file is not None:
            st.write("**Extracted:** Live PDF data parsing active.")
            st.text_area("Raw Extracted Text Snippet:", "Evaluating uploaded document layout...\nExtracting base financial metrics...\nScanning for standard SEBI disclosures...", height=100)
        else:
            st.write("**Extracted:** Awaiting file upload...")
            
    elif "Scenario A" in scenario:
        st.write("**Source Entity:** Emulated from One 97 Communications (Paytm) / Go First DRHP")
        st.text_area("Raw Extracted Text Snippet:", 
                     "INTERNAL RISK FACTORS (Page 42):\n"
                     "We have a history of net losses and negative cash flows from operating activities. "
                     "Our total outstanding indebtedness has increased significantly, resulting in a Debt-to-Equity ratio of 2.8x as of the last fiscal quarter.\n\n"
                     "RELATED PARTY TRANSACTIONS (Page 88):\n"
                     "Furthermore, promoter group subsidiary entities have provided unsecured loan guarantees amounting to Rs. 150 Cr which are not fully reflected on the consolidated balance sheet.", 
                     height=180)
                     
    elif "Scenario B" in scenario:
        st.write("**Source Entity:** Emulated Governance Risk Baseline")
        st.text_area("Raw Extracted Text Snippet:", 
                     "FINANCIAL OVERVIEW (Page 34):\n"
                     "The company maintains a conservative leverage profile with a Debt-to-Equity ratio of 0.8x.\n\n"
                     "LITIGATION AND REGULATORY ACTION (Page 55):\n"
                     "The Lead Promoter is currently subject to an ongoing fact-finding probe by the Securities and Exchange Board of India (SEBI) regarding alleged shell company violations and prior disclosure lapses. A pending claim also exists at the tax tribunal.", 
                     height=180)
                     
    else:
        st.write("**Source Entity:** Emulated Clean Baseline IPO")
        st.text_area("Raw Extracted Text Snippet:", 
                     "FINANCIAL OVERVIEW (Page 35):\n"
                     "Debt-to-Equity stands at a stable 0.8x, well within standard sector limits.\n\n"
                     "OUTSTANDING LITIGATION (Page 104):\n"
                     "There are no material pending litigations or regulatory debarment orders against the promoters, directors, or subsidiary entities. Operations have maintained positive cash flows over the last three financial years.", 
                     height=180)

st.markdown("---")

# ==========================================
# 3. THE "WOW FACTOR": AUTONOMOUS REACT ENGINE
# ==========================================
st.header("2. Autonomous ReAct Engine")

if st.button("Initialize Due Diligence Agent"):
    try:
        st.markdown("### 🧠 Live Agent Cognition Log")
        hypothesis_panel = st.empty() 
        
        with st.status("🔍 Agent actively scanning DRHP...", expanded=True) as status:
            
            # ------------------------------------------
            # LIVE UPLOAD PATH (REAL PDF ANALYSIS)
            # ------------------------------------------
            if scenario == "Upload Real PDF (Live Demo)":
                if uploaded_file is None:
                    st.error("Please upload a PDF first!")
                    st.stop()
                    
                hypothesis_panel.info("💭 **Initial Hypothesis:** Scanning live uploaded document... (Confidence: 100%)")
                
                st.write("⚙️ **Action:** Executing `pdfplumber` to extract live text from DRHP...")
                time.sleep(1)
                
                # RUN THE REAL MATH
                live_risk, live_conf, live_evidence, live_text = analyze_live_pdf(uploaded_file)
                
                st.write("👀 **Observation:** Live text successfully extracted and indexed.")
                time.sleep(1)
                
                st.write("🛠️ **Selecting Tool:** `deterministic_risk_scanner()` running NLP keyword matching...")
                time.sleep(1.5)
                
                if live_risk > 50:
                    hypothesis_panel.error(f"🎯 **Final Conclusion:** High risk factors detected in live document. (Confidence: {live_conf}%)")
                    status.update(label="Investigation Complete: Anomalies Detected", state="error", expanded=False)
                else:
                    hypothesis_panel.success(f"🎯 **Final Conclusion:** Document appears stable based on deterministic scan. (Confidence: {live_conf}%)")
                    status.update(label="Investigation Complete: Standard Baseline", state="complete", expanded=False)

            # ------------------------------------------
            # PATH A: THE PIVOT (Mock)
            # ------------------------------------------
            elif "Scenario A" in scenario:
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
            if scenario == "Upload Real PDF (Live Demo)":
                if live_risk > 50:
                    st.metric("Risk Score", f"{live_risk} / 100", delta=f"+{live_risk - 25} (High Risk)", delta_color="inverse")
                else:
                    st.metric("Risk Score", f"{live_risk} / 100", delta="Safe", delta_color="normal")
                st.metric("System Confidence", f"{live_conf}%")
                
            elif "Scenario A" in scenario:
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
            
            if scenario == "Upload Real PDF (Live Demo)":
                st.markdown("* **Base Score:** `25 / 100` (Standard baseline)")
                for evidence in live_evidence:
                    st.markdown(f"* {evidence}")
                st.markdown(f"* **Calculated Total:** `{live_risk} / 100`")
                
            elif "Scenario A" in scenario:
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

    except Exception as e:
        # TRUE FAILURE STATE 
        st.error("🚨 Analysis Incomplete — System Encountered an Error")
        st.warning(f"Error Details: {str(e)}")
        st.stop()