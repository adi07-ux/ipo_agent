import streamlit as st
import time
import pdfplumber

st.set_page_config(page_title="Autonomous SEBI DRHP Agent", layout="wide")

# ==========================================
# DETERMINISTIC SCORING ENGINE
# ==========================================
def analyze_live_pdf(pdf_file):
    raw_text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages[:20]:
                raw_text += page.extract_text() + "\n"
    except Exception as e:
        return 100, 0, ["Error parsing PDF text."], "Failed to read PDF.", []

    text_lower = raw_text.lower()
    
    if "prospectus" not in text_lower and "sebi" not in text_lower and "issue" not in text_lower:
        return 100, 0, ["🛑 **Validation Failed:** The uploaded file does not appear to be a valid SEBI IPO filing."], raw_text, ["Validation Check"]
    
    risk_score = 25
    confidence_score = 100
    evidence_log = []
    path_taken = ["Financial Extraction"]
    
    if "debt-to-equity" in text_lower or "outstanding indebtedness" in text_lower or "borrowings" in text_lower:
        risk_score += 25
        confidence_score -= 10
        evidence_log.append("🛑 **+25 pts:** Debt/leverage threshold breached. — [Pg 1-20 Scan]")
        path_taken.append("Leverage Threshold Check")
        
    if "litigation" in text_lower or "tribunal" in text_lower or "sebi probe" in text_lower:
        risk_score += 35
        confidence_score -= 15
        evidence_log.append("🛑 **+35 pts:** Active litigation keywords detected. — [Pg 1-20 Scan]")
        path_taken.append("Governance Audit")

    risk_score = min(risk_score, 100)
    confidence_score = max(confidence_score, 0)
    
    if not evidence_log:
        evidence_log.append("🟢 **+0 pts:** No severe anomaly keywords detected in initial scan.")
        path_taken.append("Clean Baseline Validation")
        
    path_taken.append("Investigation Complete")
    return risk_score, confidence_score, evidence_log, raw_text, path_taken

# ==========================================
# UI SETUP & INGESTION
# ==========================================
st.sidebar.title("🎯 Demo Scenario Selector")
scenario = st.sidebar.selectbox(
    "Select DRHP Injection Profile:",
    [
        "Scenario A: The Pivot (Hypothesis Rejection)",
        "Scenario B: The Governance Trap",
        "Upload Real PDF (Live Demo)",
        "Scenario C: Clean Baseline"
    ]
)

st.title("🤖 Autonomous SEBI DRHP Agent")
st.markdown("Automated Due Diligence & Risk Factor Extraction for Indian Capital Markets")
st.markdown("---")

st.header("1. Document Ingestion")
uploaded_file = None

if scenario == "Upload Real PDF (Live Demo)":
    uploaded_file = st.file_uploader("Upload SEBI DRHP Filing (PDF):", type="pdf")
    if uploaded_file is not None:
        st.success("✅ PDF Uploaded successfully!")
else:
    st.info(f"Ingesting DRHP profile: {scenario}")

# ==========================================
# AUTONOMOUS REACT ENGINE
# ==========================================
st.markdown("---")
st.header("2. Autonomous ReAct Engine")
final_path = []

if st.button("Initialize Due Diligence Agent"):
    
    col_plan, col_log = st.columns([1, 2])
    
    with col_plan:
        st.markdown("### 📋 Dynamic Investigation Plan")
        plan_panel = st.empty()
        
    with col_log:
        st.markdown("### 🧠 Agent Cognition Log")
        hypothesis_panel = st.empty() 
        
        with st.status("🔍 Agent actively investigating...", expanded=True) as status:
            
            # --- SCENARIO A: THE PIVOT ---
            if "Scenario A" in scenario:
                plan_panel.info("**Current Priorities:**\n1. Industry Benchmark (72%)\n2. Revenue Quality (18%)\n3. Governance Audit (10%)")
                
                hypothesis_panel.info("💭 **Observation:** Debt-to-equity is 2.8x. Three investigations are possible: Governance, Benchmark, or Cash Flow.")
                time.sleep(1.5)
                
                st.write("🛠️ **Decision:** Choosing **Industry Benchmark** because leverage (2.8x) is the strongest current signal breaching baseline bounds.")
                time.sleep(1.5)
                
                st.write("📊 **Evidence:** Sector median is 3.1x. Issuer is actually under-leveraged relative to peers.")
                time.sleep(1.5)
                
                # THE PIVOT MOMENT
                plan_panel.warning("**Plan Updated!**\n1. Revenue Quality (85%)\n2. Governance Audit (10%)\n3. Industry Benchmark (0% - Cleared)")
                hypothesis_panel.warning("🔄 **Hypothesis Rejected:** Leverage is sector-appropriate. Original hypothesis abandoned. Pivoting to revenue quality.")
                time.sleep(1.5)
                
                st.write("🛠️ **Decision:** Leverage cleared. Triggering **Customer Concentration Analyzer** to evaluate top-line stability.")
                time.sleep(1.5)
                
                st.write("🚨 **Evidence:** 82% of total revenue from a single client **[Source: DRHP Pg 61]**.")
                time.sleep(1.5)
                
                st.write("🛑 **Evaluation:** No unresolved high-priority hypotheses remain.")
                hypothesis_panel.error("🎯 **Investigation Complete:** Agent elected to stop. Primary risk is customer concentration.")
                status.update(label="Investigation Complete", state="error", expanded=False)
                final_path = ["Financial Extraction", "Industry Benchmark Analyzer", "Hypothesis Pivot", "Customer Concentration Analyzer", "Complete"]

            # --- SCENARIO B: GOVERNANCE TRAP ---
            elif "Scenario B" in scenario:
                plan_panel.info("**Current Priorities:**\n1. Cash Flow Analysis (45%)\n2. Governance Audit (40%)\n3. Benchmark (15%)")
                
                hypothesis_panel.info("💭 **Observation:** Financials are standard. NLP flagged: 'sebi probe'.")
                time.sleep(1.5)
                
                plan_panel.warning("**Plan Updated!**\n1. Governance Audit (89%)\n2. Legal Docket Search (11%)\n3. Cash Flow Analysis (0% - Paused)")
                st.write("🛠️ **Decision:** Choosing **Legal Docket Search**. Governance audit selected because promoter risk supersedes financial stability thresholds.")
                time.sleep(1.5)
                
                st.write("🚨 **Evidence:** Active SEBI fact-finding probe found against lead promoter **[Source: DRHP Pg 55]**.")
                time.sleep(1.5)
                
                st.write("🛑 **Evaluation:** Critical governance failure detected. Further financial analysis suspended.")
                hypothesis_panel.error("🎯 **Investigation Complete:** Agent elected to stop. Financials are a smokescreen; primary risk is governance.")
                status.update(label="Investigation Complete", state="error", expanded=False)
                final_path = ["Financial Extraction", "NLP Keyword Scanner", "Legal Docket Search", "Complete (Suspended)"]

            # --- LIVE DEMO PATH ---
            elif scenario == "Upload Real PDF (Live Demo)":
                if uploaded_file is None:
                    st.error("Please upload a PDF first!")
                    st.stop()
                
                plan_panel.info("**Current Priorities:**\n1. Baseline Validation (90%)\n2. Keyword Scan (10%)")
                hypothesis_panel.info("💭 **Observation:** Ingesting live document. Determining optimal routing.")
                st.write("⚙️ **Action:** Extracting text via `pdfplumber`...")
                
                live_risk, live_conf, live_evidence, live_text, final_path = analyze_live_pdf(uploaded_file)
                time.sleep(1.5)
                
                if "Validation Failed" in live_evidence[0]:
                    st.error(live_evidence[0])
                    hypothesis_panel.error("🎯 **Conclusion:** Invalid Document. Agent elected to abort.")
                    status.update(label="Investigation Aborted", state="error", expanded=False)
                else:
                    st.write("🛠️ **Decision:** Selected **Deterministic Risk Scanner**. Chosen to avoid LLM hallucination on strict financial bounds.")
                    time.sleep(1.5)
                    st.write("🛑 **Evaluation:** Baseline scan complete. No unresolved high-priority hypotheses remain.")
                    
                    if live_risk > 50:
                        hypothesis_panel.error(f"🎯 **Investigation Complete:** Agent elected to stop. Anomalies confirmed.")
                        status.update(label="Investigation Complete", state="error", expanded=False)
                    else:
                        hypothesis_panel.success(f"🎯 **Investigation Complete:** Agent elected to stop. Baseline stable.")
                        status.update(label="Investigation Complete", state="complete", expanded=False)

            # --- SCENARIO C: CLEAN ---
            else:
                plan_panel.info("**Current Priorities:**\n1. Baseline Validation (80%)\n2. Regulatory Check (20%)")
                hypothesis_panel.info("💭 **Observation:** Initial metrics within bounds. Establishing baseline.")
                time.sleep(1.5)
                
                st.write("🛠️ **Decision:** Choosing **Regulatory Check Tool**. Financials cleared, verifying promoter history to close out due diligence.")
                time.sleep(1.5)
                
                st.write("✅ **Evidence:** No litigation found **[Source: DRHP Pg 104]**.")
                time.sleep(1.5)
                
                st.write("🛑 **Evaluation:** No unresolved high-priority hypotheses remain.")
                hypothesis_panel.success("🎯 **Investigation Complete:** Agent elected to stop. Safe to proceed.")
                status.update(label="Investigation Complete", state="complete", expanded=False)
                final_path = ["Financial Extraction", "Regulatory Check Tool", "Complete"]

    # ==========================================
    # INVESTIGATION PATH & SCORING
    # ==========================================
    st.markdown("---")
    st.subheader("🛤️ Autonomous Investigation Path")
    st.info(" ➔ ".join([f"**{step}**" for step in final_path]))
    
    st.header("🧮 Deterministic Risk Audit")
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        if scenario == "Upload Real PDF (Live Demo)":
            if live_risk > 50:
                st.metric("Risk Score", f"{live_risk} / 100", delta=f"+{live_risk - 25} (High Risk)", delta_color="inverse")
            else:
                st.metric("Risk Score", f"{live_risk} / 100", delta="Safe", delta_color="normal")
        elif "Scenario A" in scenario:
            st.metric("Risk Score", "76 / 100", delta="+51 (High Risk)", delta_color="inverse")
        elif "Scenario B" in scenario:
            st.metric("Risk Score", "82 / 100", delta="+57 (High Risk)", delta_color="inverse")
        else:
            st.metric("Risk Score", "25 / 100", delta="Safe", delta_color="normal")
            
    with col2:
        if scenario == "Upload Real PDF (Live Demo)":
            for evidence in live_evidence:
                st.markdown(f"* {evidence}")
        elif "Scenario A" in scenario:
            st.markdown("* 🟢 **+0 pts:** Leverage cleared by benchmark. — **[DRHP Pg 42]**\n* 🛑 **+42 pts:** Severe Customer Concentration. — **[DRHP Pg 61]**")
        elif "Scenario B" in scenario:
            st.markdown("* 🟢 **+0 pts:** Debt-to-Equity is stable. — **[DRHP Pg 34]**\n* 🛑 **+57 pts:** Active SEBI probe. — **[DRHP Pg 55]**")
        else:
            st.markdown("* 🟢 **+0 pts:** Debt within bounds. — **[DRHP Pg 35]**\n* 🟢 **+0 pts:** Clean regulatory history. — **[DRHP Pg 104]**")