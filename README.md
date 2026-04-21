# AutoStream Lead Agent

A submission-ready Machine Learning / GenAI internship assignment project for **ServiceHive – Inflx**.

This project implements a conversational AI agent for **AutoStream**, a fictional SaaS product for automated video editing. The agent can:
- classify user intent,
- answer product and pricing questions using a **local knowledge base (RAG)**,
- detect **high-intent** users,
- collect **name, email, and creator platform**, and
- trigger a **mock lead-capture tool** only after all required fields are present.

---

## 1. Features

### Intent detection
The agent classifies the latest user message into:
- `greeting`
- `pricing_inquiry`
- `high_intent`
- `other`

### Local RAG
The agent retrieves answers from `data/knowledge_base.md`, which contains AutoStream pricing, features, and policy information.

### Multi-turn state management
The workflow preserves session state across multiple turns, including:
- previously shared name,
- email,
- creator platform,
- whether the agent is waiting for missing lead fields.

### Safe tool execution
The lead capture tool runs **only when all three values are present**:
- name
- email
- platform

### Interfaces
- CLI chat app: `app.py`
- Streamlit demo UI: `streamlit_app.py`

---

## 2. Architecture Explanation (~200 words)

I chose **LangGraph** because the assignment is fundamentally a stateful workflow rather than a single prompt-response chatbot. The user can begin with a greeting, shift into a pricing conversation, then move into a high-intent buying state where lead qualification begins. LangGraph is a strong fit because each of those steps can be represented as explicit nodes and routes, which makes the logic more reliable, easier to debug, and closer to a production agent workflow.

The graph starts with an **intent-classification node**. Based on the detected intent, the flow moves to either a greeting node, a RAG node, a lead-qualification node, or a fallback node. The RAG node retrieves grounded information from a **local Markdown knowledge base** using TF-IDF retrieval, ensuring answers remain tied to the provided product information. The lead-qualification node updates state with any extracted name, email, or creator platform and checks whether required fields are still missing.

State is managed inside the session using a structured dictionary tracked across turns. This lets the agent remember information already collected and prevents premature tool execution. The mock lead capture function is called only when all required fields are present.

---

## 3. Project Structure

```text
autostream-agent/
├── app.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .env.example
├── data/
│   └── knowledge_base.md
├── src/
│   ├── config.py
│   ├── extractor.py
│   ├── graph.py
│   ├── intent_classifier.py
│   ├── knowledge_base.py
│   ├── lead_tool.py
│   ├── nodes.py
│   ├── rag.py
│   └── state.py
└── tests/
    └── test_flow.py
```

---

## 4. How to Run Locally

### Step 1: Create a virtual environment

**Windows (PowerShell)**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Optional LLM setup
If you want richer LLM-based intent classification and responses:
1. copy `.env.example` to `.env`
2. add your OpenAI API key

If no API key is set, the app still works in offline fallback mode using rule-based classification and local retrieval.

### Step 4: Run the CLI app
```bash
python app.py
```

### Step 5: Run the Streamlit demo
```bash
streamlit run streamlit_app.py
```

---

## 5. How to Test

Run the automated tests:
```bash
pytest -q
```

### Manual test script
Use this exact flow in the app:

1. `Hi, tell me about your pricing.`
2. `What do I get in the Pro plan?`
3. `That sounds good, I want to try the Pro plan for my YouTube channel.`
4. `My name is Dhruv.`
5. `My email is dhruv@example.com`

Expected result:
- pricing answer is grounded in the knowledge base,
- platform is recognized as YouTube,
- name and email are collected across turns,
- `mock_lead_capture()` runs only after all three values are present.

---

## 6. How to Deploy

### Option A: Streamlit Community Cloud
Best for demo submission.
1. Push this repository to GitHub.
2. Create a new app in Streamlit Community Cloud.
3. Set the main file as `streamlit_app.py`.
4. Add `OPENAI_API_KEY` as a secret if using the LLM mode.

### Option B: Render / Railway
1. Push the repo to GitHub.
2. Create a new Python web service.
3. Install dependencies using `pip install -r requirements.txt`.
4. Start the app with Streamlit or wrap the agent in FastAPI for API deployment.

### Option C: Local demo for assignment
For internship submission, a local Streamlit demo plus video recording is enough and the safest route.

---

## 7. WhatsApp Deployment via Webhooks

To integrate this agent with WhatsApp in production, I would use the **WhatsApp Business API** or **Meta Cloud API**. Incoming WhatsApp messages would hit a backend webhook endpoint. That webhook would extract the user identifier and message text, then pass both into the LangGraph workflow. The user identifier would be used as the session key so the backend can restore the correct conversation state, including any previously collected lead fields.

After the agent produces a response, the backend would send the reply back through the WhatsApp API. When the agent collects all required lead details, the lead-capture step could call an internal CRM API or database writer instead of the mock tool. In a production system, I would also add session persistence, message logging, retry handling, webhook verification, and secure secret management.

---

## 8. Demo Video Plan (2–3 min)

In your screen recording, show:
1. the app starting,
2. a pricing question,
3. a grounded product answer,
4. a high-intent signal,
5. the agent asking for missing details,
6. successful lead capture,
7. optional view of the session state in Streamlit.

---

## 9. Sample Client Explanation

This project is a lightweight agentic sales workflow for AutoStream. Instead of behaving like a generic chatbot, it uses an explicit state machine to understand the user’s intent, retrieve grounded product information from a local knowledge base, and transition into lead qualification when buying intent appears. The workflow preserves memory across turns and prevents premature tool calls by validating that all required lead fields are collected first. That makes the solution more reliable, explainable, and closer to a production-ready social-to-lead assistant.

---

## 10. Notes

- The project satisfies the assignment requirements with **LangGraph-based state management**.
- The RAG layer is intentionally lightweight and local for easy evaluation.
- The LLM provider is optional so the project can still be tested offline.
