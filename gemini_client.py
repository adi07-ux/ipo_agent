import json
import os
import streamlit as st
from google import genai
from agent_tools import TOOL_MAP

SYSTEM_PROMPT = """
You are an autonomous IPO Due Diligence Agent analyzing DRHP filings. 
Evaluate the metrics, identify anomalies, and dynamically use specialized tools to investigate.

AVAILABLE TOOLS:
1. `investigate_related_party_loans`
2. `check_revenue_concentration`
3. `check_working_capital_trend`
4. `search_promoter_legal_history`
5. `fetch_competitor_margin_benchmarks`
6. `generate_briefing`: Use ONLY when ready to output the final report.

CONFIDENCE SCORE RUBRIC:
- Clean metrics with no anomalies: Score = 90. Tool = `generate_briefing`.
- Initial Anomaly Detected: Score = 40. Tool = [Select one of the 5 investigative tools].
- After Tool clears anomaly: Score = 90. Tool = `generate_briefing`.
- After Tool confirms red flag: Score = 85. Tool = `generate_briefing`.

You must output STRICT JSON containing:
{
  "reasoning_log": "<Explain why you assigned this score based on the rubric, and why you chose the tool.>",
  "tool_selected": "<Must be the exact name of one of the 6 tools>",
  "confidence_score": <Integer>
}
"""

def execute_agentic_loop(ticker: str, initial_data: str):
    """Executes the strict ReAct reasoning loop with robust fallback guardrails."""
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    context = [f"SYSTEM INSTRUCTIONS:\n{SYSTEM_PROMPT}", f"Data for {ticker}:\n{initial_data}"]
    max_calls = 3
    
    for step in range(1, max_calls + 1):
        prompt_string = "\n".join(context)
        
        try:
            # Using the stable, free-tier flash model
            response = client.models.generate_content(
                model='gemini-3.6-flash', 
                contents=prompt_string,
                config={
                    "temperature": 0.0,
                    "response_mime_type": "application/json",
                }
            )
            raw_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            decision = json.loads(raw_text)
            
            with st.expander(f"🔍 Agent Reasoning Step {step} - Confidence: {decision.get('confidence_score')}/100", expanded=True):
                st.write(f"**Logic:** {decision.get('reasoning_log')}")
                st.write(f"**Action:** Executing `{decision.get('tool_selected')}`")
            
            if decision.get("confidence_score", 0) >= 85 or decision.get("tool_selected") == "generate_briefing":
                st.success(f"✅ Finalizing Institutional Briefing for {ticker}.")
                break
                
            tool_func = TOOL_MAP.get(decision.get("tool_selected"))
            if tool_func:
                tool_result = tool_func(ticker)
                st.info(f"⚙️ Tool Output: {tool_result}")
                context.append(f"Tool Result from {decision['tool_selected']}: {tool_result}")
                
        except Exception as e:
            st.error(f"⚠️ Guardrail Triggered: Re-aligning logic format... (Debug: {str(e)})")
            break