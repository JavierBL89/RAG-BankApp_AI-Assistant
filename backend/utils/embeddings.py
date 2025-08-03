from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.schema import Document
import json, hashlib

embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
    query_instruction="Represent this query for retrieving relevant documents: {query}"
)


# build Docs into Langchain format (Document)
def load_dataSource(data: str = "data/products.json"):
     with open(data, 'r', encoding='utf-8') as file:
        items= json.load(file)
    
     docs = []
     for it in items:
        base = {
            "product": it.get("product") or it.get("product_name"),
            "category": it.get("category"),
            "url": it.get("url"),
            "lang": "en",
        }

        # 1) create One chunk per section (BEST for RAG)
        for sec in it.get("sections", []):
            title = (sec.get("section_title") or "").strip()
            content = (sec.get("content") or "").strip()
            text = (title + "\n" + content).strip()
            if len(text) < 30: # avoid short and useless chunks
                continue
            _id = hashlib.sha1((base["url"] + "|" + title + "|" + text).encode("utf-8")).hexdigest()
            docs.append(Document(page_content=text, metadata={**base, "section_title": title, "id": _id}))

        # 2) Also index the short product Description as its own task
        desc = (it.get("description") or "").strip()
        if len(desc) >= 30:
            _id = hashlib.sha1((base["url"] + "|desc|" + desc).encode("utf-8")).hexdigest()
            docs.append(Document(page_content=desc, metadata={**base, "section_title": "Product description", "id": _id})) # to avoid duplicates on rebuild.
     
     return docs