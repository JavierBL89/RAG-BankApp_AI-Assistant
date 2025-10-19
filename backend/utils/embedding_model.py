import os
import requests
from langchain_chroma import Chroma

# Hugging Face Space API endpoint for embeddings
HF_SPACE_URL = "https://huggingface.co/spaces/javierBLdev89/embedding-model_all-MiniLM-L6-v2/embed"

# --- Local paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "index", "vector_store_db"))
print("📦 Using absolute path for Chroma DB:", PERSIST_DIR)

COLLECTION = "banking_rag"


# --- Define remote embedding wrapper ---
class HFSpaceEmbedding:
    """
    Wrapper to call your Hugging Face Space API for embeddings.
    """

    def _call_api(self, texts):
        try:
            res = requests.post(HF_SPACE_URL, json={"texts": texts}, timeout=20)
            res.raise_for_status()
            data = res.json()
            return data.get("embeddings", [])
        except Exception as e:
            print("❌ Error fetching embeddings from HF Space:", e)
            return []

    def embed_query(self, text: str):
        if isinstance(text, str):
            text = [text]
        result = self._call_api(text)
        return result[0] if result else []

    def embed_documents(self, texts: list[str]):
        return self._call_api(texts)


# --- Initialize embeddings ---
embeddings = HFSpaceEmbedding()

