import streamlit as st
import time
import pdfplumber
import json
import google.generativeai as genai

st.set_page_config(page_title="Autonomous SEBI DRHP Agent", layout="wide")

# ==========================================
# BALANCED DETERMINISTIC FALLBACK ENGINE
# ==========================================
def analyze_live_pdf_fallback(raw_text, total_pages, scan_limit):
    """A balanced deterministic rule-based checker to prevent false 100/100 spikes."""
    text_lower = raw_text.lower()
    
    risk_score = 25
    evidence_coverage = 90
    evidence_log = []
    path_taken = ["Financial Extraction"]
    primary_driver = "None Detected"
    
    if "debt-to-equity" in text_lower or "outstanding indebtedness" in text_lower or "borrowings" in text_lower:
        risk_score += 20
        evidence_coverage -= 5
        evidence_log.append(f"🛑 **+20 pts:** Significant indebtedness disclosures found. — [Scanned Pg 1-{scan_limit}]")
        path_taken.append("Leverage Threshold Check")
        primary_driver = "Capital Structure / Leverage"
        
    if "sebi probe" in text_lower or "show cause notice" in text_lower or "debarment" in text_lower or "litigation" in text_lower:
        risk_score += 30
        evidence_coverage -= 10
        evidence_log.append(f"🛑 **+30 pts:** Regulatory or legal action keywords flagged. — [Scanned Pg 1-{scan_limit}]")
        path_taken.append("Governance Audit")
        primary_driver = "Governance & Regulatory"
        
    if "negative cash flows from operating activities" in text_lower or "net loss" in text_lower or "net losses" in text_lower:
        risk_score += 15
        evidence_coverage -= 5
        evidence_log.append(f"🛑 **+15 pts:** Operating loss disclosures confirmed. — [Scanned Pg 1-{scan_limit}]")
        path_taken.append("Cash Flow Analysis")
        if primary_driver == "None Detected":
            primary_driver = "Operational Cash Flow"

    risk_score = min(risk_score, 100)
    evidence_coverage = max(evidence_coverage, 0)
    
    if len(evidence_log) == 0:
        evidence_log.append(f"🟢 **+0 pts:** Standard regulatory disclosures observed. — [Scanned Pg 1-{scan_limit}]")
        path_taken.append("Clean Baseline Validation")
        primary_driver = "Standard Baseline"
        
    path_taken.append("Investigation Complete")
    return risk_score, evidence_coverage, evidence_log, path_taken, total_pages, primary_driver

# ==========================================
# PRIMARY LLM AGENT
# ==========================================
def analyze_live_pdf(pdf_file):
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
        return 100, 0, ["Error parsing PDF text."], "Failed to read PDF.", [], True, 0, "Parse Error"

    text_lower = raw_text.lower()
    if "prospectus" not in text_lower and "sebi" not in text_lower and "issue" not in text_lower:
        return 100, 0, ["🛑 **Validation Failed:** The uploaded file does not appear to be a valid SEBI IPO filing."], raw_text, ["Validation Check"], False, total_pages, "Validation Failed"
    
    api_key = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass

    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            You are an autonomous financial due diligence agent. Analyze this SEBI DRHP excerpt.
            Evaluate for: 1. Leverage/Debt anomalies, 2. Promoter Litigation, 3. Negative Cash Flow.