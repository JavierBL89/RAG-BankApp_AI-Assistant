from langchain_chroma import Chroma
from backend.utils.embedding_model import hfembeddings
from backend.utils.chunk_data import load_dataSource
import shutil
from collections import Counter
import os

# Use an absolute path (works both locally and on Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "index", "vector_store_db")) # Directory where the Chroma vector store is persisted
COLLECTION = "banking_rag"
print("📦 Using absolute path for vectore_db:", PERSIST_DIR)


if not os.path.exists(PERSIST_DIR):
    raise RuntimeError(f"❌ Chroma path not found: {PERSIST_DIR}")
else:
    print(f"✅ Chroma path found: {PERSIST_DIR}")

# This script builds a Chroma vector store index for the banking knowledge base.
def build_chroma():
    docs = load_dataSource()
    vs= Chroma(
        collection_name=COLLECTION,
        embedding_function=hfembeddings,
        persist_directory=PERSIST_DIR,
    )

    #Upsert withouyt duplicates
        # Drop duplicate docs by ID (keep first)
    seen = set()
    unique_docs = []
    unique_ids = []
    ids = [d.metadata.get("id") for d in docs]

    for doc, doc_id in zip(docs, ids):
        if doc_id not in seen:
            seen.add(doc_id)
            unique_docs.append(doc)
            unique_ids.append(doc_id)

    if len(unique_docs) < len(docs):
        print(f"🧹 Removed {len(docs) - len(unique_docs)} duplicate documents")

    try:
        vs.add_documents(documents=unique_docs, ids=unique_ids)
        print("Added documents in Chroma.")
        
    except Exception as e:
        print("⚠️ Failed to update documents:", e)

    print(f"Indexed {len(docs)} documents into Chroma at {PERSIST_DIR}")
    

if __name__ == "__main__":
    shutil.rmtree(PERSIST_DIR + "/chroma.sqlite3", ignore_errors=True) # deletes the existing Chroma DB every time
    build_chroma()
    print("Chroma index built successfully.")