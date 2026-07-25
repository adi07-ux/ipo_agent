def investigate_related_party_loans(ticker: str) -> str:
    """Investigates hidden debt structures and promoter loans."""
    return f"CRITICAL FINDING: {ticker} has 150 Cr in undisclosed related-party loans to promoter entities at 0% interest, inflating the baseline Debt-to-Equity ratio."

def check_revenue_concentration(ticker: str) -> str:
    """Analyzes top-line revenue reliance on key clients."""
    return f"RISK DETECTED: Top 3 clients contribute 62% of {ticker}'s total consolidated revenue for FY25."

def check_working_capital_trend(ticker: str) -> str:
    """Evaluates cash flow versus revenue growth."""
    return f"WARNING: {ticker} shows aggressive revenue recognition, but operating cash flow is deeply negative (-45 Cr)."

def search_promoter_legal_history(ticker: str) -> str:
    """Checks for SEBI regulatory bans or pending court cases."""
    return f"FLAG: Promoter group for {ticker} has ongoing tax disputes of INR 85 Crores pending before the High Court."

def fetch_competitor_margin_benchmarks(ticker: str) -> str:
    """Compares EBITDA margins to industry peers."""
    return f"BENCHMARK: {ticker}'s EBITDA margin compressed to 11.5%, significantly below the industry average of 18.2%."

def generate_briefing(ticker: str) -> str:
    """Finalizes the investigation."""
    return "Final Due Diligence Memo Ready."

# Tool Registry for the ReAct Loop
TOOL_MAP = {
    "investigate_related_party_loans": investigate_related_party_loans,
    "check_revenue_concentration": check_revenue_concentration,
    "check_working_capital_trend": check_working_capital_trend,
    "search_promoter_legal_history": search_promoter_legal_history,
    "fetch_competitor_margin_benchmarks": fetch_competitor_margin_benchmarks,
    "generate_briefing": generate_briefing
}