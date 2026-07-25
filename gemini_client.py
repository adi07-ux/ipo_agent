import time
import os
import google.generativeai as genai

# Setup Gemini API (ensure your key is securely stored in Streamlit secrets)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
model = genai.GenerativeModel('gemini-1.5-flash')

def call_model_with_retries(prompt, max_retries=3):
    """
    Calls the Gemini API using exponential backoff to handle 
    temporary 503 or 429 server overload errors.
    """
    base_delay = 2  # Start with a 2-second wait
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_str = str(e).lower()
            
            # Check if the error is a temporary server capacity issue
            if "503" in error_str or "unavailable" in error_str or "high demand" in error_str or "429" in error_str:
                if attempt == max_retries - 1:
                    # Retries exhausted, escalate the crash to the UI
                    raise Exception(f"API unavailable after {max_retries} attempts.")
                
                # Exponential backoff: waits 2s, then 4s, then 8s...
                sleep_time = base_delay * (2 ** attempt)
                print(f"API overloaded. Silently retrying in {sleep_time}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(sleep_time)
            else:
                # If it's a different error (like an invalid API key), crash immediately
                raise e

def execute_agentic_loop(extracted_text, scenario):
    """
    Main reasoning loop passing the extracted text to the API.
    """
    prompt = f"Analyze this DRHP text: {extracted_text[:500]}..."
    response = call_model_with_retries(prompt)
    return response

# ---------------------------------------------------------
# EXTERNAL TOOL FUNCTIONS 
# ---------------------------------------------------------
def investigate_related_party_loans():
    return "Critical Finding - 150 Cr hidden promoter debt confirmed."

def generate_briefing():
    return "Institutional briefing prepared."