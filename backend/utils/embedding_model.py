from langchain_huggingface import HuggingFaceEmbeddings
import os

HF_TOKEN= os.getenv("HF_TOKEN")

embeddings = HuggingFaceEmbeddings(
    api_key=HF_TOKEN,
    model_name="BAAI/bge-m3",
    encode_kwargs={"normalize_embeddings": True}
)