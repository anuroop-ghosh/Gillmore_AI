# Gillmore_AI

## 🧠 System Architecture & Data Flow

This project utilizes an event-driven, agentic workflow to handle document ingestion and retrieval without manual intervention.

```mermaid
sequenceDiagram
    participant User
    participant n8n as n8n (Docker)
    participant API as FastAPI Webhook
    participant Brain as LangChain & Embeddings
    participant DB as ChromaDB
    participant UI as Streamlit UI

    %% Ingestion Pipeline
    rect rgb(230, 240, 255)
    Note over User, DB: Phase 1: Automated Event-Driven Ingestion
    User->>n8n: Drops PDF in Local Folder
    n8n->>API: HTTP POST (Binary Stream)
    API->>Brain: Triggers ingest_file()
    Brain->>Brain: Chunks Document
    Brain->>DB: Generates & Stores Vectors (Gemini/Ollama)
    end

    %% Retrieval Pipeline
    rect rgb(240, 255, 240)
    Note over User, UI: Phase 2: Retrieval-Augmented Generation (RAG)
    User->>UI: Asks Question
    UI->>DB: Similarity Search Query
    DB-->>UI: Returns Relevant Context
    UI->>Brain: Passes Context + Query to LLM
    Brain-->>UI: Streams Final Answer
    end