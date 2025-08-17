from langchain_community.vectorstores import Chroma
from utils.embedding_model  import embeddings

PERSIST_DIR = "data/index/"
COLLECTION = "banking_rag"


# Function to get retrievers from Chroma vector store
def get_retreivers(user_quey:str, query_intent: dict):

    k = 5  # Number of top results to return
    vs = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )

    # where is a metadata filter, e.g., {"category": "Mortgages"} or {"product":"First Time Buyer"}
    return vs.as_retreiver(search_type="similarity", search_kwargs={"k": k, "filter":user_quey})


if __name__ == "__main__":
    r= get_retreivers(k=5, where={"category": "Mortgages"})
    for data_source in r.invoke("How do I know what I can borrow?"):
        print(data_source.metadata.get("product"), data_source.page_content)
        print("URL:", data_source.metadata.get("url"))
        print("---", data_source.page_content[:200], "...\n")
