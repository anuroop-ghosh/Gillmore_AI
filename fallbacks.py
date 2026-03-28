from langchain_core.embeddings import Embeddings

class FallbackEmbeddings(Embeddings):
    def __init__(self, embeddings_list: list[Embeddings]):
        if not embeddings_list:
            raise ValueError("Must provide at least one embeddings model.")
        self.embeddings_list = embeddings_list

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        last_error = None
        for i, embedder in enumerate(self.embeddings_list):
            try:
                return embedder.embed_documents(texts)
            except Exception as e:
                print(f"⚠️ Embedding model {i+1} failed: {e}. Trying fallback...")
                last_error = e

        raise RuntimeError(f"All fallback embedding models failed! Last error: {last_error}")

    def embed_query(self, text: str) -> list[float]:
        last_error = None
        for i, embedder in enumerate(self.embeddings_list):
            try:
                return embedder.embed_query(text)
            except Exception as e:
                print(f"⚠️ Embedding query {i+1} failed: {e}. Trying fallback...")
                last_error = e

        raise RuntimeError(f"All fallback embedding models failed! Last error: {last_error}")
