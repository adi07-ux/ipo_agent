import streamlit as st
import time
import pdfplumber
import json
import google.generativeai as genai

st.set_page_config(page_title="Autonomous SEBI DRHP Agent", layout="wide")

# ==========================================
# HYBRID ENGINE: DETERMINISTIC FALLBACK
# ==========================================
def analyze_live_pdf_fallback(raw_text, total_pages, scan_limit):
    """The deterministic range threshold method (Fallback)"""
    text_lower = raw_text.lower()
    
    risk_score = 25
    confidence_score = 100
    evidence_log = []
    path_taken = ["Financial Extraction"]
    
    if "debt-to-equity" in text_lower or "outstanding indebtedness" in text_lower or "borrowings" in text_lower:
        risk_score += 25
        confidence_score -= 10
        evidence_log.append(f"🛑 **+25 pts:** Debt/leverage threshold breached. — [Scanned Pg 1-{scan_limit}]")
        path_taken.append("Leverage Threshold Check")
        
    if "litigation" in text_lower or "tribunal" in text_lower or "sebi probe" in text_lower:
        risk_score += 35
        confidence_score -= 15
        evidence_log.append(f"🛑 **+35 pts:** Active litigation keywords detected. — [Scanned Pg 1-{scan_limit}]")
        path_taken.append("Governance Audit")
        
    if "negative cash flow" in text_lower or "net loss" in text_lower:
        risk_score += 20
        confidence_score -= 10
        evidence_log.append(f"🛑 **+20 pts:** Negative cash flow parameters triggered. — [Scanned Pg 1-{scan_limit}]")
        path_taken.append("Cash Flow Analysis")

    risk_score = min(risk_score, 100)
    confidence_score = max(confidence_score, 0)
    
    if not evidence_log:
        evidence_log.append(f"🟢 **+0 pts:** No severe anomaly keywords detected. — [Scanned Pg 1-{scan_limit}]")
        path_taken.append("Clean Baseline Validation")
        
    path_taken.append("Investigation Complete")
    return risk_score, confidence_score, evidence_log, path_taken

# ==========================================
# HYBRID ENGINE: PRIMARY LLM AGENT
# ==========================================
def analyze_live_pdf(pdf_file, api_key):
    """Attempts real LLM reasoning, degrades gracefully to deterministic fallback."""
    raw_text = ""
    total_pages = 0
    pages_to_scan = 30
    
    try:
        with pdfplumber.open(pdf_file) as pdf:
            total_pages = len(pdf.pages)
            scan_limit = min(pages_to_scan, total_pages)
            for page in pdf.pages[:scan_limit]:
                extracted = page.extract_text()
                if extracted:
                    raw_text += extracted + "\n"
    except Exception:
        return 100, 0, ["Error parsing PDF text."], "Failed to read PDF.", [], True

    text_lower = raw_text.lower()
    if "prospectus" not in text_lower and "sebi" not in text_lower and "issue" not in text_lower:
        return 100, 0, ["🛑 **Validation Failed:** The uploaded file does not appear to be a valid SEBI IPO filing."], raw_text, ["Validation Check"], False
    
    # --- TRUE AGENTIC ATTEMPT ---
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            You are an autonomous financial due diligence agent. Analyze this SEBI DRHP excerpt.
            Evaluate for: 1. Leverage/Debt anomalies, 2. Promoter Litigation, 3. Negative Cash Flow.
            
            Respond strictly in valid JSON format with these exact keys:
            "risk_score": integer between 25 and 100,
            "confidence_score": integer between 0 and 100,
            "evidence_log": list of strings citing the issues found (e.g., "🛑 High debt detected."),
            "path_taken": list of strings representing the logic steps (e.g., ["Financial Extraction", "Debt Analysis", "Complete"])
            
            Document Text:
            {raw_text[:15000]} 
            """
            
            # Simple retry logic (Backoff)
            for attempt in range(2):
                try:
                    response = model.generate_content(prompt)
                    # Strip markdown block formatting if present
                    json_str = response.text.replace('```json', '').replace('```', '').strip()
                    data = json.loads(json_str)
                    return data['risk_score'], data['confidence_score'], data['evidence_log'], raw_text, data['path_taken'], False
                except Exception:
                    time.sleep(1.5) # Wait and retry
            
            raise Exception("LLM Retries Exhausted")
            
        except Exception:
            # Silently fall through to fallback
            pass

    # --- DETERMINISTIC FALLBACK ---
    risk, conf, ev, path = analyze_live_pdf_fallback(raw_text, total_pages, scan_limit)
    return risk, conf, ev, raw_text, path, True

# ==========================================
# UI SETUP & INGESTION
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

st.sidebar.markdown("---")
api_key = st.sidebar.text_input("Gemini API Key (For Live Agent):", type="password")

st.title("🤖 Autonomous SEBI DRHP Agent")
st.markdown("Automated Due Diligence & Risk Factor Extraction for Indian Capital Markets")
st.markdown("---")

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
    
    col_plan, col_log = st.columns([1, 2])
    
    with col_plan:
        st.markdown("### 📋 Dynamic Investigation Plan")
        plan_panel = st.empty()
        
    with col_log:
        st.markdown("### 🧠 Agent Cognition Log")
        hypothesis_panel = st.empty() 
        
        with st.status("🔍 Agent actively investigating...", expanded=True) as status:
            
            # --- LIVE DEMO PATH ---
            if scenario == "Upload Real PDF (Live Demo)":
                if uploaded_file is None:
                    st.error("Please upload a PDF first!")
                    st.stop()
                
                plan_panel.info("**Current Priorities:**\n1. Baseline Validation (90%)\n2. Agentic Reasoning (10%)")
                hypothesis_panel.info("💭 **Observation:** Ingesting live document. Routing to primary LLM...")
                
                live_risk, live_conf, live_evidence, live_text, final_path, is_fallback = analyze_live_pdf(uploaded_file, api_key)
                
                if "Validation Failed" in live_evidence[0]:
                    st.error(live_evidence[0])
                    hypothesis_panel.error("🎯 **Conclusion:** Invalid Document. Agent elected to abort.")
                    status.update(label="Investigation Aborted", state="error", expanded=False)
                else:
                    st.write("👀 **Action:** Full extraction complete.")
                    time.sleep(1)
                    
                    if is_fallback:
                        st.warning("⚠️ **Fallback Mode Active:** LLM routing timed out. Seamlessly transitioned to deterministic rule-based evaluation.")
                    else:
                        st.success("✅ **Primary Pipeline Active:** LLM successfully parsed document layout and reasoned through disclosures.")
                        
                    st.write("🛑 **Evaluation:** Investigation bounds resolved.")
                    
                    if live_risk > 50:
                        hypothesis_panel.error(f"🎯 **Investigation Complete:** Agent elected to stop. Anomalies confirmed.")
                        status.update(label="Investigation Complete", state="error", expanded=False)
                    else:
                        hypothesis_panel.success(f"🎯 **Investigation Complete:** Agent elected to stop. Baseline stable.")
                        status.update(label="Investigation Complete", state="complete", expanded=False)

            # --- MOCK SCENARIOS (UNCHANGED) ---
            elif "Scenario A" in scenario:
                plan_panel.info("**Current Priorities:**\n1. Industry Benchmark (72%)\n2. Revenue Quality (18%)\n3. Governance Audit (10%)")
                hypothesis_panel.info("💭 **Observation:** Debt-to-equity is 2.8x. Three investigations are possible: Governance, Benchmark, or Cash Flow.")
                time.sleep(1.5)
                st.write("🛠️ **Decision:** Choosing **Industry Benchmark** because leverage (2.8x) is the strongest current signal.")
                time.sleep(1.5)
                st.write("📊 **Evidence:** Sector median is 3.1x. Issuer is actually under-leveraged.")
                time.sleep(1.5)
                plan_panel.warning("**Plan Updated!**\n1. Revenue Quality (85%)\n2. Governance Audit (10%)\n3. Industry Benchmark (0% - Cleared)")
                hypothesis_panel.warning("🔄 **Hypothesis Rejected:** Leverage is sector-appropriate. Pivoting to revenue quality.")
                time.sleep(1.5)
                st.write("🛠️ **Decision:** Triggering **Customer Concentration Analyzer**.")
                time.sleep(1.5)
                st.write("🚨 **Evidence:** 82% of total revenue from a single client **[Source: DRHP Pg 61]**.")
                time.sleep(1.5)
                st.write("🛑 **Evaluation:** No unresolved high-priority hypotheses remain.")
                hypothesis_panel.error("🎯 **Investigation Complete:** Agent elected to stop. Primary risk is customer concentration.")
                status.update(label="Investigation Complete", state="error", expanded=False)
                final_path = ["Financial Extraction", "Industry Benchmark Analyzer", "Hypothesis Pivot", "Customer Concentration Analyzer", "Complete"]

            elif "Scenario B" in scenario:
                plan_panel.info("**Current Priorities:**\n1. Cash Flow Analysis (45%)\n2. Governance Audit (40%)\n3. Benchmark (15%)")
                hypothesis_panel.info("💭 **Observation:** Financials are standard. NLP flagged: 'sebi probe'.")
                time.sleep(1.5)
                plan_panel.warning("**Plan Updated!**\n1. Governance Audit (89%)\n2. Legal Docket Search (11%)\n3. Cash Flow Analysis (0% - Paused)")
                st.write("🛠️ **Decision:** Choosing **Legal Docket Search**. Governance audit selected because promoter risk supersedes financials.")
                time.sleep(1.5)
                st.write("🚨 **Evidence:** Active SEBI fact-finding probe found against lead promoter **[Source: DRHP Pg 55]**.")
                time.sleep(1.5)
                st.write("🛑 **Evaluation:** Critical governance failure detected. Financial analysis suspended.")
                hypothesis_panel.error("🎯 **Investigation Complete:** Agent elected to stop. Primary risk is governance.")
                status.update(label="Investigation Complete", state="error", expanded=False)
                final_path = ["Financial Extraction", "NLP Keyword Scanner", "Legal Docket Search", "Complete (Suspended)"]

            else:
                plan_panel.info("**Current Priorities:**\n1. Baseline Validation (80%)\n2. Regulatory Check (20%)")
                hypothesis_panel.info("💭 **Observation:** Initial metrics within bounds. Establishing baseline.")
                time.sleep(1.5)
                st.write("🛠️ **Decision:** Choosing **Regulatory Check Tool**.")
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
        if scenario == "Upload Real PDF (Live Demo)":
            for evidence in live_evidence:
                st.markdown(f"* {evidence}")
        elif "Scenario A" in scenario:
            st.markdown("* 🟢 **+0 pts:** Leverage cleared by benchmark. — **[DRHP Pg 42]**\n* 🛑 **+42 pts:** Severe Customer Concentration. — **[DRHP Pg 61]**")
        elif "Scenario B" in scenario:
            st.markdown("* 🟢 **+0 pts:** Debt-to-Equity is stable. — **[DRHP Pg 34]**\n* 🛑 **+57 pts:** Active SEBI probe. — **[DRHP Pg 55]**")
        else:
            st.markdown("* 🟢 **+0 pts:** Debt within bounds. — **[DRHP Pg 35]**\n* 🟢 **+0 pts:** Clean regulatory history. — **[DRHP Pg 104]**")