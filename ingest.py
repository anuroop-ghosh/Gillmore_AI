import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from uuid import uuid4
from models import Models

# Load environment variables (like GOOGLE_API_KEY) from .env file
load_dotenv() 

# --- Model Selection Switch ---
models = Models()

# 1. Select the Embeddings model (Gemini)
# Change 'embeddings_gemini' to 'embeddings_ollama' to switch to Ollama
embeddings = models.embeddings_gemini 

# 2. Select the LLM (Gemini) - used for the RAG part, though not directly in this ingestion script
# Change 'model_gemini' to 'model_ollama' to switch to Ollama
llm = models.model_gemini 

# --- Configuration (No Change) ---
data_folder = "./data"
chunk_size = 1000
chunk_overlap = 50
check_interval = 10

# --- Vector Store Initialization (No Change) ---
# The vector store now uses the selected 'embeddings' object (Gemini by default)
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chroma_langchain_db",
)

# --- Ingestion Functions (No Change) ---
def ingest_file(file_path):
    if not file_path.lower().endswith('.pdf'):
        print(f"Skipping non-PDF file: {file_path}")
        return

    print(f"Starting to ingest file: {file_path}")
    loader = PyPDFLoader(file_path)
    loaded_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n", " ", ""]
    )

    documents = text_splitter.split_documents(loaded_documents)
    uuids = [str(uuid4()) for _ in range(len(documents))]
    print(f"Adding {len(documents)} documents to the vector store")
    vector_store.add_documents(documents=documents, ids=uuids)
    print(f"Finished ingesting file: {file_path}")

def main_loop():
    while True:
        files_processed = False

        for filename in os.listdir(data_folder):
            if filename.startswith(".") or filename.startswith("!"):
                continue
            file_path=os.path.join(data_folder, filename)
            ingest_file(file_path)
            new_filename = "!" + filename
            new_file_path = os.path.join(data_folder, new_filename)
            os.rename(file_path, new_file_path)

            files_processed = True
        if not files_processed:
            print("No new files found. Ingestion complete. Exiting.")
            break
        time.sleep(check_interval)

if __name__ == "__main__":
    main_loop()
