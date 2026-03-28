# Gillmore_AI
## 🧠 System Architecture & Data Flow

This project utilizes an event-driven, agentic workflow to handle document ingestion and retrieval without manual intervention.

```mermaid
flowchart LR
    subgraph Ingestion Pipeline
        direction TB
        A([📄 Drop PDF in Folder]) -->|Triggers| B[⚙️ n8n Workflow Node]
        B -->|Binary Stream| C[🌐 FastAPI Webhook]
        C -->|ingest_file| D[🧠 LangChain Embeddings]
        D -->|Store Vectors| E[(🗄️ ChromaDB)]
    end

    subgraph Chat Retrieval
        direction TB
        F([👤 User Asks Question]) --> G[💻 Streamlit UI]
        G -->|Similarity Search| E
        E -.->|Provide Context| H[🤖 Gemini/Ollama LLM]
        H -.->|Stream Answer| G
    end