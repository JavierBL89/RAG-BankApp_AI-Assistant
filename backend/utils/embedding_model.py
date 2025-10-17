import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("❌ HF_TOKEN not found")

hfembeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=HF_TOKEN,
    model_name="BAAI/bge-m3",
    encode_kwargs={"normalize_embeddings": True}
)


