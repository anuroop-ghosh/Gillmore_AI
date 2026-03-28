# Gillmore AI
## 🧠 System Architecture & Agentic Workflow

This project utilizes an event-driven, agentic workflow, leveraging separate components for automated ingestion and advanced retrieval.

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': { 'mainBkg': '#1a1d21', 'mainStr': '#54a3ff', 'clusterBkg': '#121417', 'clusterStr': '#3a3f44' }}}%%
flowchart LR
    subgraph "🤖 Ingestion Agent (Automated)"
        direction TB
        A{{📄 <b>New Document</b>}} -->|Event-Driven Ingestion| B(n8n.io Workflow Node)
        B -->|Multipart/Form-Data| C([🌐 FastAPI Webhook])
    end

    C -->|Triggers| D[🧠 LangChain Embeddings<br/>multimodal]
    D -->|Persistent Vectors| E[(🗄️ ChromaDB Vector Store)]

    subgraph "🤖 Retrieval Agent (Interactive)"
        direction TB
        F{{👤 User Query}} --> G[💻 Streamlit Chat Interface]
        G -->|Similarity Search| E
        E -.->|Relevant Context| H[[🤖 LLM Engine Gemini/Ollama]]
        H -.->|RAG-Enhanced Answer| G
    end

    %% Styles
    classDef trigger fill:#fff3cd,stroke:#e6db55,color:#856404;
    classDef agent fill:#cfe2f3,stroke:#6aa84f,color:#0c343d;
    classDef storage fill:#d4edda,stroke:#28a745,color:#155724;
    
    class A,F trigger;
    class D,H agent;
    class E storage;
