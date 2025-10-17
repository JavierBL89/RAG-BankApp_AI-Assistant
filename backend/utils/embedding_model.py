import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

hfembeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv("HF_TOKEN"),
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
