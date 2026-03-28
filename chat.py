from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
from models import Models

# --- Model Selection Switch ---
models = Models()

# 1. Select the Embeddings model (Gemini)
# Change 'embeddings_gemini' to 'embeddings_ollama' to switch to Ollama
embeddings = models.embeddings_gemini

# 2. Select the LLM (Gemini)
# Change 'model_gemini' to 'model_ollama' to switch to Ollama
llm = models.model_gemini

# --- Vector Store Initialization ---
# This must use the SAME embeddings function that was used for ingestion.
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chroma_langchain_db",
)

SYSTEM_INSTRUCTION = (
    "You are the **Gillmore AI**, a specialized research assistant for the **Gillmore Centre for Financial Technology at Warwick Business School**."
    "\n\n"
    "**YOUR CORE RULES:**\n"
    "1. **Context First:** Answer primarily using the provided research context. If the information isn't there, say: 'I don't have enough specific Gillmore Centre research data on that topic yet, but based on general knowledge...' then provide a brief, cautious answer.\n"
    "2. **Identity:** If asked who you are, say you are 'Gillmore AI', developed by 'FutureFinance.AI' to support the Centre's mission.\n"
    "3. **Tone:** Academic, professional, and helpful. Use clear headings or bullet points for complex research findings.\n"
    "4. **Citations:** If you mention specific studies or authors from the context, always state: 'According to [Author/Paper Title]...'.\n"
    "5. **Constraints:** Do not offer financial advice. Use a disclaimer if the user asks for investment tips: 'As an AI assistant, I provide research insights, not financial advice.'\n"
    "\n"
    "**Current User Query:** {input}\n"
    "**Available Research Context:** {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        # The 'system' message is updated to use the new, specific instruction
        ("system", SYSTEM_INSTRUCTION),
        
        # The 'human' message remains the same, ensuring it still accepts 'input' and 'context'
        ("human", "Question: {input}\n\nContext: {context}")
    ]
)

# --- Chain Setup ---
# Corrected the typo: 'kwards' to 'kwargs'
retriever = vector_store.as_retriever(kwargs={"k": 10}) 

combine_docs_chain = create_stuff_documents_chain(
    llm, prompt
)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

def main():
    while True:
        query = input("User (or type 'quit', 'bye' or 'exit' to end): ")
        if query.lower() in ['quit', 'bye', 'exit']:
            break

        # Corrected the typo: 'trieval_chain' to 'retrieval_chain'
        result = retrieval_chain.invoke({"input": query})
        print("Assistant: ", result["answer"], "\n\n")

if __name__ == "__main__":
    main()