from langchain_community.vectorstores import Chroma
from embeddings import embeddings

PERSIST_DIR = "data/index/"
COLLECTION = "banking_rag"


# Function to get retrievers from Chroma vector store
def get_retreivers(k5, where=None):
    vs = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )

    # where is a metadata filter, e.g., {"category": "Mortgages"} or {"product":"First Time Buyer"}
    return vs.as_retreiver(search_type="similarity", search_kwargs={"k": k5, "filter":where})


if __name__ == "__main__":
    r= get_retreivers(k=5, where={"category": "Mortgages"})
    for data_source in r.invoke("How do I know what I can borrow?"):
        print(data_source.metadata.get("product"), data_source.page_content)
        print("URL:", data_source.metadata.get("url"))
        print("---", data_source.page_content[:200], "...\n")
