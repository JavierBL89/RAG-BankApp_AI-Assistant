from langchain_chroma import Chroma
from utils.embedding_model  import embeddings
import os
PERSIST_DIR = "data/index/vector_store_db"  # Directory where the Chroma vector store is persisted
COLLECTION = "banking_rag"


# Function to get retrievers from Chroma vector store
def get_retrievers():
    """
      Retrieve documents from Chroma vector store.
    """
    print("📁 Using persist directory:", os.path.abspath(PERSIST_DIR))

    k = 5  # Number of top results to return
    # load the vector store
    vs = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )
    print(f"Collection name: {vs._collection.name}")
    print(f"Number of documents: {vs._collection.count()}")
        ### MaxMarginalRelevanceRetriever (from LangChain), which diversifies results by reducing redundancy:
    # return vs.as_retriever(search_type="mmr", search_kwargs={"k": k})

    return vs.as_retriever(search_type="similarity", search_kwargs={"k": k})

async def retrieve_similar_docs(all_queries: list[str]):
    """
    Retrieve similar documents based on the query.
    """
    merged_query = " ".join(all_queries)  # Merge all queries into a single string for one-shot retrieval

    # get datasource
    retrieved_datasource = get_retrievers()
    context = await retrieved_datasource.ainvoke(merged_query)
    
    return context



if __name__ == "__main__":
    r= get_retrievers(k=5, where={"category": "Mortgages"})
    for data_source in r.invoke("How do I know what I can borrow?"):
        print(data_source.metadata.get("product"), data_source.page_content)
        print("URL:", data_source.metadata.get("url"))
        print("---", data_source.page_content[:200], "...\n")
