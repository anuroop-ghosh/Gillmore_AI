import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from fallbacks import FallbackEmbeddings

class Models:
    def __init__(self):
        self.embeddings_ollama = OllamaEmbeddings(
            model="mxbai-embed-large"
        )

        self.model_ollama = ChatOllama(
            model = "llama3.2",
            temperature = 0,
        )

        # --- Gemini Model ---
        # Note: API Key picked up from "GOOGLE_API_KEY" automatically.
        
        # 1. Embeddings Model with Fallback Loop
        primary_embed = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
        backup_embed = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        self.embeddings_gemini = FallbackEmbeddings(
            embeddings_list=[primary_embed, backup_embed]
        )

        # 2. LLM Model
        #Primary
        primary_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        #Backup
        backup_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        self.model_gemini = primary_llm.with_fallbacks([backup_llm])
