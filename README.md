# Horizon Campus AI Advisor — Agentic RAG System

An enterprise-grade, multi-agent AI application designed to assist students and staff of Horizon Campus by retrieving accurate information from official student handbooks and academic guidelines. Built as part of the **IT41043 - Intelligent Systems (Agentic AI)** module[cite: 1].

---

## 🚀 Live Demo & Links
* **Live Streamlit App:** [Access Streamlit Cloud App](https://horizon-agentic-ai-zcw9pruuvf4uucqwradnr.streamlit.app)[cite: 1]
* **GitHub Repository:** [isuruchathushka724-dev/horizon-agentic-ai](https://github.com/isuruchathushka724-dev/horizon-agentic-ai)[cite: 1]

---

## 🏛️ System Architecture & Design Patterns
The application implements an advanced multi-agent architecture leveraging three distinct agentic design patterns[cite: 1]:
1. **Orchestrator-Worker Pattern:** A central orchestrator manages user requests, delegates sub-tasks, and handles final synthesis.
2. **Intent Router Pattern:** Automatically classifies user queries (e.g., academic rules, degree paths, or administrative guidelines) to route them effectively.
3. **Fallback & Tool-Use Pattern:** Handles domain-specific document retrieval via vector search and seamlessly falls back to general knowledge or clarifying questions when context is missing.

### Architecture Flow Diagram
    [ User Query ] 
           │
           ▼
    [ Streamlit UI ] ──> [ Orchestrator Agent ] ──> [ Intent Router ]
                                                           │
                                                           ▼
                                             [ Chroma Vector Store (RAG) ]
                                                           │
                                                           ▼
                                                 [ Retrieved Context ]
                                                           │
                                                           ▼
                                             [ Advisor Agent (Synthesis) ]
                                                           │
                                                           ▼
                                                [ Final UI Response ]

---

## 🤖 Agent-to-Agent Communication Protocol
The system utilizes at least two distinct agents (Orchestrator Agent and Academic Advisor Agent) that exchange structured messages using a custom JSON-based protocol over LangChain execution layers[cite: 1].

    [ Orchestrator Agent ] 
           │ (Sends Structured JSON Payload: query, intent, constraints)
           ▼
    [ Academic Advisor Agent ] 
           │ (Returns Processed Context & Synthesized Answer)
           ▼
    [ Orchestrator Agent ] ──> Final UI Render

---

## 📊 Model Selection Strategy
To optimize latency, cost, and reasoning capability, the system deliberately selects two distinct models across Groq and OpenRouter[cite: 1]:

| Sub-task | Model (Provider) | Why Chosen (Cost, Latency, Context, Reasoning) |
| :--- | :--- | :--- |
| **Intent Routing / Classification** | `Llama 3.1 8B (Groq)`[cite: 1] | Ultra-low latency, near-free cost per token, and highly efficient for fast text classification and routing decisions[cite: 1]. |
| **Deep Reasoning & Synthesis** | `Llama 3.3 70B (Groq)`[cite: 1] | High reasoning quality and larger context window, justifying the processing trade-off for accurate final student advisory responses[cite: 1]. |

---

## 📚 RAG Pipeline & Retrieval Evaluation
* **Corpus & Chunking:** Ingests the official Horizon Campus Student Handbook PDF. Documents are split using recursive character text splitters to maintain semantic coherence.
* **Vector Store & Embeddings:** Utilizes **ChromaDB** as the local vector store powered by HuggingFace embeddings[cite: 1].

### Retrieval Evaluation (5 Sample Queries)
1. **Query:** *"What is the minimum attendance required to sit for exams?"*  
   * **Result:** Successfully retrieved the 80% mandatory attendance chunk[cite: 1]. Relevant and accurate.
2. **Query:** *"Who is the Chief Executive Officer of the campus?"*  
   * **Result:** Accurately extracted the section naming Mr. Periyasamy Saravanan[cite: 1]. Relevant.
3. **Query:** *"What sports facilities are available?"*  
   * **Result:** Extracted the complete list of sports (Basketball, Cricket, Swimming, etc.) directly from campus guidelines[cite: 1]. Relevant.
4. **Query:** *"Are mobile phones allowed in the examination hall?"*  
   * **Result:** Retrieved specific disciplinary clauses regarding prohibited items during exams[cite: 1]. Relevant.
5. **Query:** *"What IT degree programs are offered?"*  
   * **Result:** Retrieved BSc (Hons) in Information Technology, Data Science, and Cyber Security paths[cite: 1]. Relevant.

---

## ⚙️ Installation & Local Setup

1. **Clone the repository:**
   git clone https://github.com/isuruchathushka724-dev/horizon-agentic-ai.git
   cd horizon-agentic-ai

2. **Create and activate a virtual environment:**
   python -m venv venv
   # On Windows:
   venv\Scripts\activate

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Configure Secrets:**
   Create a .streamlit/secrets.toml file or set environment variables:
   GROQ_API_KEY = "your_groq_api_key_here"

5. **Run the application:**
   streamlit run app.py

---

## ⚠️ Known Limitations
* The vector search is restricted to the provided Student Handbook corpus; queries outside institutional policies rely on fallback general knowledge.
* PDF formatting variations can occasionally affect table parsing within chunking splits.

---

## 🛡️ Academic Integrity
This submission is an original work designed, built, and deployed by Isuru Chathushka under academic guidelines for Horizon Campus[cite: 1]. All external libraries and models are explicitly documented.