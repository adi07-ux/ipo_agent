import json

def investigate_related_party_loans(ticker: str) -> str:
    if ticker == "CLEAN_IPO":
        return json.dumps({"finding": "Related party loans account for < 2% of total debt. Fully secured."})
    elif ticker == "RISKY_IPO":
        return json.dumps({"finding": "🚨 HIGH RISK: 65% of corporate debt is held by promoter-owned shell entities."})
    return json.dumps({"finding": "Data unavailable."})

def check_revenue_concentration(ticker: str) -> str:
    if ticker == "CLEAN_IPO":
        return json.dumps({"finding": "Top 10 customers account for a healthy 18% of total revenue."})
    elif ticker == "RISKY_IPO":
        return json.dumps({"finding": "🚨 HIGH RISK: Top 3 customers account for 74% of total revenue."})
    return json.dumps({"finding": "Data unavailable."})

def check_working_capital_trend(ticker: str) -> str:
    return json.dumps({"finding": "Working capital is stable across the last 3 fiscal years."})

def search_promoter_legal_history(ticker: str) -> str:
    return json.dumps({"finding": "No material civil or criminal litigation pending against promoters."})

import json

def investigate_related_party_loans(ticker: str) -> str:
    if ticker == "CLEAN_IPO":
        return json.dumps({"finding": "Related party loans account for < 2% of total debt. Fully secured."})
    elif ticker == "RISKY_IPO":
        return json.dumps({"finding": "🚨 HIGH RISK: 65% of corporate debt is held by promoter-owned shell entities."})
    return json.dumps({"finding": "Data unavailable."})

def check_revenue_concentration(ticker: str) -> str:
    if ticker == "CLEAN_IPO":
        return json.dumps({"finding": "Top 10 customers account for a healthy 18% of total revenue."})
    elif ticker == "RISKY_IPO":
        return json.dumps({"finding": "🚨 HIGH RISK: Top 3 customers account for 74% of total revenue."})
    return json.dumps({"finding": "Data unavailable."})

def check_working_capital_trend(ticker: str) -> str:
    return json.dumps({"finding": "Working capital is stable across the last 3 fiscal years."})

def search_promoter_legal_history(ticker: str) -> str:
    return json.dumps({"finding": "No material civil or criminal litigation pending against promoters."})

def fetch_competitor_margin_benchmarks(ticker: str) -> str:
    if ticker == "CLEAN_IPO":
        return json.dumps({"finding": "Target margins (22%) are in line with sector average (21%)."})
    elif ticker == "RISKY_IPO":
        return json.dumps({"finding": "🚨 HIGH RISK: Target margins (12%) severely lag sector average (18.5%)."})
    return json.dumps({"finding": "Data unavailable."})

# Mapping dictionary for the execution loop to call functions dynamically
TOOL_MAP = {
    "investigate_related_party_loans": investigate_related_party_loans,
    "check_revenue_concentration": check_revenue_concentration,
    "check_working_capital_trend": check_working_capital_trend,
    "search_promoter_legal_history": search_promoter_legal_history,
    "fetch_competitor_margin_benchmarks": fetch_competitor_margin_benchmarks,
    "generate_briefing": lambda ticker: json.dumps({"status": "ready to generate report"})}
def fetch_competitor_margin_benchmarks(ticker: str) -> str:
    if ticker == "CLEAN_IPO":
        return json.dumps({"finding": "Target margins (22%) are in line with sector average (21%)."})
    elif ticker == "RISKY_IPO":
        return json.dumps({"finding": "🚨 HIGH RISK: Target margins (12%) severely lag sector average (18.5%)."})
    return json.dumps({"finding": "Data unavailable."})

# Mapping dictionary for the execution loop to call functions dynamically
TOOL_MAP = {
    "investigate_related_party_loans": investigate_related_party_loans,
    "check_revenue_concentration": check_revenue_concentration,
    "check_working_capital_trend": check_working_capital_trend,
    "search_promoter_legal_history": search_promoter_legal_history,
    "fetch_competitor_margin_benchmarks": fetch_competitor_margin_benchmarks,
    "generate_briefing": lambda ticker: json.dumps({"status": "ready to generate report"})
}