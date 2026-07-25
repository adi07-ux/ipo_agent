import json
import os
import streamlit as st
from google import genai
from agent_tools import TOOL_MAP

SYSTEM_PROMPT = """
You are an autonomous IPO Due Diligence Agent analyzing DRHP filings. 
Evaluate the metrics, identify anomalies, and dynamically use specialized tools to investigate.

AVAILABLE TOOLS:
1. `investigate_related_party_loans`: Use if debt is unusually high (>1.5x) or promoter debt is flagged.
2. `check_revenue_concentration`: Use if top-line revenue looks overly dependent on a few clients.
3. `check_working_capital_trend`: Use if cash flow is negative while revenue is growing.
4. `search_promoter_legal_history`: Use if legal proceedings or promoter pledging are mentioned.
5. `fetch_competitor_margin_benchmarks`: Use if EBITDA margins are compressing or highly volatile.
6. `generate_briefing`: Use ONLY when you are ready to stop investigating and output the final report.

CONFIDENCE SCORE RUBRIC (STRICT ENFORCEMENT):
Round 0 (Initial Base Metrics Review):
- If metrics are clean with no anomalies: Score = 90. Tool = `generate_briefing`.
- If anomaly detected: Score = 40. Tool = [Select one of the 5 investigative tools].

Round 1 (After 1st Tool Result):
- If Tool 1 clears the anomaly: Score = 90. Tool = `generate_briefing`.
- If Tool 1 confirms severe red flag: Score = 85. Tool = `generate_briefing`.
- If Tool 1 is ambiguous: Score = 50. Tool = [Select a 2nd tool].

Round 2 (After 2nd Tool Result):
- If Tool 2 clears anomalies: Score = 90. Tool = `generate_briefing`.
- If Tool 2 confirms red flag: Score = 85. Tool = `generate_briefing`.
- If Tool 2 is STILL ambiguous: Score = 60. Tool = [Select a 3rd tool].

Round 3 (Max Depth Reached):
- Max limit hit. Score = 85. Tool = `generate_briefing`.

You must output STRICT JSON containing:
{
  "reasoning_log": "<Explain why you assigned this score based on the rubric, and why you chose the tool.>",
  "tool_selected": "<Must be the exact name of one of the 6 tools>",
  "confidence_score": <Integer>
}
"""

def get_gemini_decision_with_retry(context_messages: list, retries: int = 2) -> dict:
    """Calls Gemini, forces JSON output, and retries if parsing fails."""
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    prompt_string = "\n".join(context_messages)
    
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',  # Switched to the widely supported 2.0 model
                contents=prompt_string,
                config={  # Switched to a dictionary config to prevent import issues
                    "temperature": 0.0,
                    "response_mime_type": "application/json",
                }
            )
            raw_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
            return json.loads(raw_text)
            
        except Exception as e:
            if attempt == 0:
                # We added {str(e)} here so the UI prints the EXACT error causing the failure!
                st.warning(f"⚠️ Re-aligning agent logic... (Debug Error: {str(e)})")
                context_messages.append("System Error: Invalid JSON output. Output strictly valid JSON.")
                continue
                
    # Transparent Fallback if model fails completely
    return {
        "reasoning_log": "System Error: Investigation incomplete due to an LLM parsing error. Proceeding with partial data.",
        "tool_selected": "generate_briefing",
        "confidence_score": 60
    }

def run_agentic_loop(ticker: str, initial_metrics: str):
    """The main ReAct execution loop with a hard 3-call ceiling."""
    context = [
        f"SYSTEM INSTRUCTIONS:\n{SYSTEM_PROMPT}", 
        f"Initial Metrics for {ticker}: {initial_metrics}"
    ]
    
    max_calls = 3
    current_calls = 0
    
    while current_calls < max_calls:
        # 1. Ask Gemini for the next action
        decision = get_gemini_decision_with_retry(context)
        
        # 2. Print logic to the Streamlit UI immediately
        st.write(f"**Confidence:** {decision['confidence_score']}/100")
        st.write(f"**Agent Logic:** {decision['reasoning_log']}")
        st.write(f"**Action:** Executing `{decision['tool_selected']}`")
        st.divider()
        
        # 3. Stop Condition
        if decision["confidence_score"] >= 85 or decision["tool_selected"] == "generate_briefing":
            break
            
        # 4. Execute the chosen tool
        tool_func = TOOL_MAP.get(decision["tool_selected"])
        if tool_func:
            tool_result = tool_func(ticker)
            context.append(f"Tool Result from {decision['tool_selected']}: {tool_result}")
        
        current_calls += 1