# 🤖 Autonomous SEBI DRHP Agent
Automated Due Diligence & Risk Factor Extraction for Indian Capital Markets

 📌 The Problem
Evaluating a 300+ page SEBI Draft Red Herring Prospectus (DRHP) is a massive operational bottleneck for investment banks and retail investors, typically requiring 5+ hours of manual reading. Furthermore, standard "chat-with-PDF" AI wrappers are not viable for high-stakes finance because they act as "black boxes"—they hallucinate facts, lack page-level citations, and catastrophically crash during live deployments if API rate limits are hit.

💡 Our Solution
The Autonomous SEBI DRHP Agent acts as an automated junior financial analyst. It ingests complex IPO filings, executes a ReAct (Reasoning and Acting) investigation loop, and outputs an institutional-grade **AI Investment Brief**.

🚀 Key Features & Our "Moat"
* **Hybrid Resilience Architecture:** Built for enterprise deployment, not just a hackathon stage. If the primary LLM pipeline experiences network latency or JSON parsing failures, the system catches the error and seamlessly degrades into a **Deterministic Fallback Engine**, ensuring a compliance-ready output 100% of the time.
* **Auditable Evidence Tracking:** Separates "How risky is this company?" (Risk Score) from "How much evidence was verified?" (Evidence Coverage). Every critical anomaly flagged includes a direct citation to the source document.
* **Agentic Dynamic Memory:** The system maintains an active memory state, tracking facts learned, rejected hypotheses, and shifting priorities (e.g., pivoting from capital structure analysis to governance risks based on NLP keyword flags).
* **Domain-Specific Context Bounding:** Physically restricts the extraction engine to the Executive Summary and Internal Risk Factors, eliminating "boilerplate hallucinations" and reducing API latency to under 5 seconds.

🛠️ Tech Stack

* **Frontend/State Management:** Streamlit
* **Primary Intelligence:** Google Gemini 3.6 Flash (via `google-generativeai`)
* **Document Ingestion:** `pdfplumber`
* **Data Protocol:** Constrained JSON formatting

📸 System Overview

*(⚠️ HACKATHON TIP: Insert a screenshot of your beautiful final UI dashboard here! Just drag and drop an image of the "AI Investment Brief" into GitHub.)*

⚙️ How to Run Locally

Follow these steps to test the agent on your local machine.

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/sebi-drhp-agent.git
cd sebi-drhp-agent

```

**2. Install dependencies**

```bash
pip install streamlit pdfplumber google-generativeai

```

**3. Configure Streamlit Secrets (API Key)**
To run the primary LLM pipeline, you must provide a Google Gemini API key securely.
Create a `.streamlit` folder in the root directory, and inside it, create a `secrets.toml` file:

```bash
mkdir .streamlit
touch .streamlit/secrets.toml

```

Add your key to `secrets.toml`:

```toml
GEMINI_API_KEY = "your_actual_api_key_here"

```

**4. Launch the application**

```bash
streamlit run app.py

```

---

## 🧮 How the Architecture Works

1. **Ingestion:** User uploads a SEBI DRHP PDF. `pdfplumber` extracts the critical layout-aware text, bounding it to the first 30 pages to avoid boilerplate traps.
2. **Primary Route (LLM):** The payload is sent to Gemini 1.5 Flash with strict instructions to return a structured JSON schema evaluating Leverage, Litigation, and Cash Flow.
3. **Resilience Route (Fallback):** If the API key is missing, rate-limited, or times out after 2 backoff retries, the system routes the text to a deterministic NLP keyword scanner. This engine calculates risk mathematically based on hardcoded governance and financial triggers.
4. **Synthesis:** The UI dynamically renders the Agent Cognition Log, Evidence Rigor metrics, and the final Executive Investment Brief.
