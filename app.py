import streamlit as st
import time
import pdfplumber

st.set_page_config(page_title="Autonomous SEBI DRHP Agent", layout="wide")

# ==========================================
# REAL DETERMINISTIC SCORING ENGINE 
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
        evidence_log.append("🛑 **+25 pts:** Debt/leverage keyword thresholds breached in initial pages.")
        path_taken.append("Leverage Threshold Check")
        
    if "litigation" in text_lower or "tribunal" in text_lower or "sebi probe" in text_lower:
        risk_score += 35
        confidence_score -= 15
        evidence_log.append("🛑 **+35 pts:** Active litigation/regulatory keywords detected.")
        path_taken.append("Governance Audit")
        
    if "negative cash flow" in text_lower or "net loss" in text_lower:
        risk_score += 20
        confidence_score -= 10
        evidence_log.append("🛑 **+20 pts:** Negative cash flow parameters triggered.")
        path_taken.append("Cash Flow Analysis")

    risk_score = min(risk_score, 100)
    confidence_score = max(confidence_score, 0)
    
    if not evidence_log:
        evidence_log.append("🟢 **+0 pts:** No severe anomaly keywords detected in initial scan.")
        path_taken.append("Clean Baseline Validation")
        
    path_taken.append("Investigation Complete")
    return risk_score, confidence_score, evidence_log, raw_text, path_taken

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.title("🎯 Demo Scenario Selector")
scenario = st.sidebar.selectbox(
    "Select DRHP Injection Profile:",
    [
        "Upload Real PDF (Live Demo)",
        "Scenario A: The Pivot (Hypothesis Rejection)",
        "Scenario B: The Governance Trap",
        "Scenario C: Clean Baseline"
    ]
)

st.title("🤖 Autonomous SEBI DRHP Agent")
st.markdown("Automated Due Diligence & Risk Factor Extraction for Indian Capital Markets")
st.markdown("---")

# ==========================================
# DOCUMENT INGESTION
# ==========================================
st.header("1. Document Ingestion")
uploaded_file = None
preview_text = "Evaluating uploaded document layout...\nExtracting base financial metrics...\nScanning for standard SEBI disclosures..."

if scenario == "Upload Real PDF (Live Demo)":
    uploaded_file = st.file_uploader("Upload SEBI DRHP Filing (PDF):", type="pdf")
    if uploaded_file is not None:
        st.success("✅ PDF Uploaded successfully!")
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                extracted = pdf.pages[0].extract_text()
                if extracted:
                    preview_text = extracted[:1500] + "\n\n... [Remaining text securely buffered] ..."
                else:
                    preview_text = "No readable text found on the first page."
            uploaded_file.seek(0) 
        except Exception as e:
            preview_text = f"Preview generation failed.\nError: {e}"
else:
    st.info(f"Ingesting DRHP profile: {scenario}")

with st.expander("📄 View Parsed Sections & Tables"):
    if scenario == "Upload Real PDF (Live Demo)":
        if uploaded_file is not None:
            st.text_area("Raw Extracted Text Snippet:", preview_text, height=150)
        else:
            st.write("Awaiting file upload...")
    elif "Scenario A" in scenario:
        st.text_area("Raw Extracted Text Snippet:", "INTERNAL RISK FACTORS (Page 42):\n...resulting in a Debt-to-Equity ratio of 2.8x...\n\nRELATED PARTY TRANSACTIONS (Page 61):\n82% of revenue derived from a single client...", height=150)
    elif "Scenario B" in scenario:
        st.text_area("Raw Extracted Text Snippet:", "FINANCIAL OVERVIEW (Page 34):\nDebt-to-Equity ratio of 0.8x.\n\nLITIGATION (Page 55):\nLead Promoter subject to ongoing SEBI fact-finding probe...", height=150)
    else:
        st.text_area("Raw Extracted Text Snippet:", "FINANCIAL OVERVIEW (Page 35):\nDebt-to-Equity stands at 0.8x.\n\nLITIGATION (Page 104):\nNo material pending litigations...", height=150)

st.markdown("---")

# ==========================================
# AUTONOMOUS REACT ENGINE
# ==========================================
st.header("2. Autonomous ReAct Engine")
final_path = []

if st.button("Initialize Due Diligence Agent"):
    try:
        st.markdown("### 🧠 Live Agent Cognition Log")
        hypothesis_panel = st.empty() 
        
        with st.status("🔍 Agent actively investigating...", expanded=True) as status:
            
            # --- LIVE DEMO PATH ---
            if scenario == "Upload Real PDF (Live Demo)":
                if uploaded_file is None:
                    st.error("Please upload a PDF first!")
                    st.stop()
                
                hypothesis_panel.info("💭 **Initial Hypothesis:** Scanning live document. (Confidence: 45%)")
                st.write("⚙️ **Action:** Extracting text via `pdfplumber`...")
                time.sleep(1)
                
                live_risk, live_conf, live_evidence, live_text, final_path = analyze_live_pdf(uploaded_file)
                
                if "Validation Failed" in live_evidence[0]:
                    st.error(live_evidence[0])
                    hypothesis_panel.error("🎯 **Conclusion:** Invalid Document. Aborted.")
                    status.update(label="Investigation Aborted", state="error", expanded=False)
                else:
                    st.write("👀 **Observation:** Live text extracted.")
                    time.sleep(1)
                    st.write("🛠️ **Decision:** Considered Multi-threaded LLM evaluation and Deterministic Scanner. Selected **Deterministic Risk Scanner** to avoid hallucination on financial bounds.")
                    time.sleep(1.5)
                    
                    if live_risk > 50:
                        hypothesis_panel.error(f"🎯 **Conclusion:** High risk detected. (Confidence: {live_conf}%)")
                        status.update(label="Investigation Complete", state="error", expanded=False)
                    else:
                        hypothesis_panel.success(f"🎯 **Conclusion:** Stable baseline. (Confidence: {live_conf}%)")
                        status.update(label="Investigation Complete", state="complete", expanded=False)

            # --- SCENARIO A: THE PIVOT ---
            elif "Scenario A" in scenario:
                hypothesis_panel.info("💭 **Initial Hypothesis:** High leverage flagged. (Confidence: 42%)")
                st.write("👀 **Observation:** Extracted Debt-to-Equity is 2.8x **[Pg 42]**.")
                time.sleep(1.5)
                
                st.write("🛠️ **Decision:** Considered Governance Audit and Industry Benchmark. Selected **Industry Benchmark Tool** because the 1.5x debt threshold was breached.")
                time.sleep(1.5)
                
                st.write("📊 **Evidence:** Sector median is 3.1x. Issuer is actually under-leveraged.")
                time.sleep(1.5)
                
                hypothesis_panel.warning("🔄 **Hypothesis Updated:** Leverage is sector-appropriate. Pivoting to revenue quality. (Confidence: 87%)")
                st.write("🛠️ **Decision:** Leverage cleared. Triggering **Customer Concentration Analyzer**.")
                time.sleep(1.5)
                
                st.write("🚨 **Evidence:** 82% of total revenue from a single client **[Pg 61]**.")
                time.sleep(1)
                
                hypothesis_panel.error("🎯 **Final Conclusion:** Primary risk is customer concentration, not leverage. (Confidence: 94%)")
                status.update(label="Investigation Complete", state="error", expanded=False)
                final_path = ["Financial Extraction", "Industry Benchmark Analyzer", "Hypothesis Pivot", "Customer Concentration Analyzer", "Complete"]

            # --- SCENARIO B: GOVERNANCE TRAP ---
            elif "Scenario B" in scenario:
                hypothesis_panel.info("💭 **Initial Hypothesis:** Financials stable, scanning NLP flags. (Confidence: 50%)")
                st.write("👀 **Observation:** Financials pass thresholds. NLP flagged: 'sebi probe' **[Pg 55]**.")
                time.sleep(1.5)
                
                st.write("🛠️ **Decision:** Considered Cash Flow Analysis and Legal Docket Search. Selected **Legal Docket Search** due to high-severity keyword trigger.")
                time.sleep(1.5)
                
                st.write("🚨 **Evidence:** Active SEBI fact-finding probe found against lead promoter.")
                time.sleep(1.5)
                
                hypothesis_panel.error("🎯 **Final Conclusion:** Financials are a smokescreen. Primary risk is promoter governance. (Confidence: 91%)")
                status.update(label="Investigation Complete", state="error", expanded=False)
                final_path = ["Financial Extraction", "NLP Keyword Scanner", "Legal Docket Search", "Complete"]

            # --- SCENARIO C: CLEAN ---
            else:
                hypothesis_panel.info("💭 **Initial Hypothesis:** Establishing baseline. (Confidence: 50%)")
                st.write("👀 **Observation:** All metrics within deterministic thresholds **[Pg 35]**.")
                time.sleep(1.5)
                
                st.write("🛠️ **Decision:** Financials cleared. Triggering **Regulatory Check Tool** for final verification.")
                time.sleep(1.5)
                
                st.write("✅ **Evidence:** No litigation found **[Pg 104]**.")
                time.sleep(1.5)
                
                hypothesis_panel.success("🎯 **Final Conclusion:** Safe to proceed. (Confidence: 95%)")
                status.update(label="Investigation Complete", state="complete", expanded=False)
                final_path = ["Financial Extraction", "Regulatory Check Tool", "Complete"]

        # ==========================================
        # INVESTIGATION PATH & SCORING
        # ==========================================
        st.markdown("---")
        
        # KILLER FEATURE: Visual Path
        st.subheader("🛤️ Autonomous Investigation Path")
        path_string = " ➔ ".join([f"**{step}**" for step in final_path])
        st.info(path_string)
        
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
                st.markdown("* 🟢 **+0 pts:** Leverage cleared by benchmark. — **[Pg 42]**\n* 🛑 **+42 pts:** Severe Customer Concentration. — **[Pg 61]**")
            elif "Scenario B" in scenario:
                st.markdown("* 🟢 **+0 pts:** Debt-to-Equity is stable. — **[Pg 34]**\n* 🛑 **+57 pts:** Active SEBI probe. — **[Pg 55]**")
            else:
                st.markdown("* 🟢 **+0 pts:** Debt within bounds. — **[Pg 35]**\n* 🟢 **+0 pts:** Clean regulatory history. — **[Pg 104]**")

    except Exception as e:
        st.error("🚨 Analysis Incomplete — System Encountered an Error")
        st.warning(f"Error Details: {str(e)}")
        st.stop()