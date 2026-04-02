# AgenticArXiv

> 5 specialized AI agents. A complete research report from arXiv papers in under 60 seconds.

![Status: Local Complete](https://img.shields.io/badge/Status-Local_Complete-green)
![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Frontend: Next.js](https://img.shields.io/badge/Frontend-Next.js_16-000000)
![AI: Gemini Flash](https://img.shields.io/badge/AI-Gemini_1.5_Flash-8E75B2)

## What it does
AgenticArXiv is an autonomous research orchestration system. It ingests complex academic papers from arXiv into a local FAISS vector store, and coordinates five specialized LLM agents to produce structured, highly technical research reports covering:
1. Literature Review
2. Methodology Comparison
3. Results Analysis
4. Critical Assessment
5. Final Synthesis

## Architecture Flow

1. **Ingestion (ETL):** Fetches PDFs from the arXiv XML API, extracts text via `pypdf`, and creates 500-word chunks (with 50-word semantic overlaps).
2. **Embedding:** Compresses text into 768-dimensional vectors using Gemini's `text-embedding-004` (strictly utilizing the `retrieval_document` task type projection).
3. **Retrieval (RAG):** Performs exact L2 distance similarity searches against the FAISS index to pull the 15 most semantically relevant chunks.
4. **Mixture-of-Agents (MoA) Orchestration:** A FastAPI controller fires 5 distinct Gemini 1.5 Flash agents sequentially. Each agent receives a uniquely formatted context window filtered by specific keywords to match its system persona.
5. **Client Presentation:** A Next.js 16 application polls the backend, renders dynamic loading skeletons during the 40+ second orchestration phase, and parses the final LLM output into styled, collapsible Markdown cards.

## Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **LLM Orchestrator** | Gemini 1.5 Flash | Fast inference, large context window |
| **Embeddings** | Gemini `text-embedding-004` | 768-dim semantic projection |
| **Backend Framework** | Python 3.13 / FastAPI | Asynchronous I/O, strict Pydantic type safety |
| **Vector Database** | FAISS (`IndexFlatL2`) | Exact L2 similarity search, local persistence |
| **Observability** | Langfuse | Distributed tracing, span latencies, token counting |
| **Frontend Framework** | Next.js 16 (App Router) | Client-side routing, Turbopack, React state management |
| **Styling & UI** | Tailwind CSS v4, Lucide React | Utility-first styling, developer-tool aesthetic |

## Design Decisions & Trade-offs

### Why 5 specialized agents over one big prompt?
Each agent has a focused system prompt, keyword-filtered context, and task-appropriate temperature. For instance, the Results Agent requires mathematical precision (temperature=0.2), while the Synthesis Agent requires generative breadth (temperature=0.4). A single monolithic prompt forces all these constraints to compete, degrading output quality.

### The Dimension Guard (768-dim)
FAISS indexes are dimension-locked at creation. Mixing legacy OpenAI embeddings (1536-dim) with Gemini embeddings (768-dim) results in silent retrieval failure. To prevent this, the `FAISSStore` implements a strict dimension guard and positional assertions to guarantee vector metadata synchronization.

### Sequential vs. Parallel Execution
Agents are fired sequentially rather than via `asyncio.gather`. While parallel execution is faster, hitting the Gemini API with 5 concurrent requests frequently triggers Free Tier `429 RESOURCE_EXHAUSTED` rate limits. Sequential execution provides higher reliability in constrained environments.

---

## Local Setup Instructions

### Prerequisites
* Python 3.11+
* Node.js 18+
* [Google AI Studio API Key](https://aistudio.google.com/)
* [Langfuse API Keys](https://cloud.langfuse.com/)

### 1. Backend Setup
```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure Environment Variables
cp .env.example .env
# Add GEMINI_API_KEY, LANGFUSE_PUBLIC_KEY, and LANGFUSE_SECRET_KEY to .env

# Start FastAPI Server
uvicorn agenticarxiv.api.server:app --reload
