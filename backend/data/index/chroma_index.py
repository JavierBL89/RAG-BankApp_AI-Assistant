from langchain_community.vectorstores import Chroma
from utils.embedding_model import embeddings
from utils.chunk_data import load_dataSource



PERSIST_DIR = "data/index"
COLLECTION = "banking_rag"

# This script builds a Chroma vector store index for the banking knowledge base.
def build_chroma():
    docs = load_dataSource()
    vs= Chroma(
        collection_name=COLLECTION,
        embeding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )

    #Upsert withouyt duplicates
    ids = [d.metadata.get("id") for d in docs]
    vs.add_documents(docs, ids=ids)  #Re-running with same content won’t duplicate because we pass stable ids.
    #Persist the index to disk
    vs.persist()
    print(f"Indexed {len(docs)} documents into Chroma at {PERSIST_DIR}")
    

if __name__ == "__main__":
    build_chroma()
    print("Chroma index built successfully.")