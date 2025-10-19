import os
from langchain_chroma import Chroma
import requests
from utils.embedding_model import embeddings

# Hugging Face Space API URL
HF_SPACE_URL = "https://huggingface.co/spaces/javierBLdev89/embedding-model_all-MiniLM-L6-v2"  # Replace with your Hugging Face Space URL


# Build an absolute path that works both locally and on Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "index", "vector_store_db")) # Chroma persistent directory
print("📦 Using absolute path for Chroma DB:", PERSIST_DIR)

COLLECTION = "banking_rag"



# --- Create Chroma retriever ---
def get_retrievers(k: int = 5, where: dict | None = None):
    print("📁 Using persist directory:", PERSIST_DIR)

    vs = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,  # pass the HF wrapper instance
        persist_directory=PERSIST_DIR,
    )

    print(f"Collection name: {vs._collection.name}")
    print(f"Number of documents: {vs._collection.count()}")

    return vs.as_retriever(search_type="similarity", search_kwargs={"k": k, "filter": where})


def retrieve_similar_docs(all_queries: list[str]):
    merged_query = " ".join(all_queries).strip()
    retriever = get_retrievers(k=5)
    relevant_retrieved_docs = retriever.invoke(merged_query) # <-- text travels through the pipeline HERE 

    filtered_docs = [
        doc for doc in relevant_retrieved_docs
        if merged_query.lower() in doc.metadata.get("product", "").lower()
    ]

    context_docs = filtered_docs[:1] if filtered_docs else relevant_retrieved_docs[:1]
    return context_docs


if __name__ == "__main__":
    retriever = get_retrievers(k=5, where={"category": "Mortgages"})
    results = retriever.invoke("How do I know what I can borrow?")
    for doc in results:
        print(doc.metadata.get("product"), doc.page_content[:200])
        print("URL:", doc.metadata.get("url"))
        print("---\n")