# AutoStream Lead Agent

A conversational AI sales assistant built with **LangGraph** for a fictional SaaS product called **AutoStream**. The agent answers product-related questions using a local knowledge base, understands user intent, remembers conversation context across multiple messages, and captures leads only after collecting all required information.

The project was built as part of a Machine Learning / Generative AI internship assignment and focuses on building a structured, stateful workflow instead of a prompt-only chatbot.

---

## Highlights

* Multi-turn conversation with persistent session state
* Intent classification for user messages
* Local RAG using a Markdown knowledge base
* High-intent lead qualification workflow
* Safe lead capture with field validation
* Optional OpenAI integration with offline fallback
* CLI and Streamlit interfaces
* Unit tests for conversation flow

---

## Features

### Intent Classification

The agent classifies incoming messages into one of the following categories:

* Greeting
* Pricing Inquiry
* High Intent
* Other

The detected intent determines which workflow node is executed next.

### Retrieval-Augmented Generation (RAG)

Product information is retrieved from a local Markdown knowledge base (`data/knowledge_base.md`) using TF-IDF retrieval. This keeps responses grounded in the available documentation without requiring a vector database.

### Conversation Memory

The workflow stores information collected during the conversation, including:

* Name
* Email address
* Creator platform
* Pending fields required for lead capture

This allows users to provide information naturally across multiple messages without repeating themselves.

### Lead Qualification

When the user shows buying intent, the agent begins collecting lead information. The lead capture tool is executed only after all required fields have been collected.

Required fields:

* Name
* Email
* Creator Platform

---

## Architecture

The project uses **LangGraph** to model the conversation as a stateful workflow.

Instead of relying on a single prompt, each responsibility is handled by a dedicated node. This keeps the logic easier to understand, test, and extend.

The workflow follows this sequence:

```text
User Message
      │
      ▼
Intent Classification
      │
      ├── Greeting
      ├── Pricing
      ├── High Intent
      └── Other
              │
              ▼
      Knowledge Retrieval
              │
              ▼
      Lead Qualification
              │
              ▼
      Mock Lead Capture
```

Session state is shared across the workflow so previously collected information is available throughout the conversation.

---

## Project Structure

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

## Tech Stack

* Python
* LangGraph
* Streamlit
* OpenAI API (optional)
* scikit-learn
* TF-IDF
* python-dotenv
* pytest

---

## Installation

Clone the repository and create a virtual environment.

### Windows

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages.

```bash
pip install -r requirements.txt
```

---

## Configuration

The project can run in two modes.

### Offline Mode

No additional configuration is required. Intent classification and retrieval use local implementations.

### OpenAI Mode (Optional)

Copy the example environment file.

```bash
cp .env.example .env
```

Add your API key.

```env
OPENAI_API_KEY=your_api_key
```

If no API key is provided, the application automatically falls back to offline mode.

---

## Running the Project

### Command Line

```bash
python app.py
```

### Streamlit Interface

```bash
streamlit run streamlit_app.py
```

---

## Running Tests

Execute the test suite using:

```bash
pytest -q
```

---

## Example Conversation

```
User: Hi, tell me about your pricing.

Assistant:
Provides pricing information from the knowledge base.

User:
What do I get in the Pro plan?

Assistant:
Retrieves and explains the Pro plan features.

User:
That sounds good. I want to use it for my YouTube channel.

Assistant:
Recognizes high purchase intent and asks for missing lead details.

User:
My name is Dhruv.

Assistant:
Stores the name and asks for the email address.

User:
My email is dhruv@example.com

Assistant:
Stores the email, detects the creator platform (YouTube), and triggers the mock lead capture tool.
```

---

## Deployment

The Streamlit application can be deployed directly to **Streamlit Community Cloud** by connecting the GitHub repository and selecting `streamlit_app.py` as the entry point.

The project can also be deployed to platforms such as **Render** or **Railway**. Since the conversation logic is separated from the interface, it can easily be wrapped with a FastAPI service for API-based deployments if needed.

---

## Future Improvements

Possible enhancements include:

* Vector database support for larger knowledge bases
* Persistent storage for conversation history
* CRM integration for real lead management
* WhatsApp Business API integration
* Analytics dashboard for conversations and conversions
* Improved entity extraction using LLMs

---

## License

This project is intended for educational and demonstration purposes.
