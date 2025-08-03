import requests
import numpy as np
import os

HEADERS = { "Authorization": f"Bearer {os.getenv('HF_API_KEY')}" }
HF_MODEL_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/BAAI/bge-m3"


def embed_text(text):
    payload= {"inputs": text, "options": {"wait_for_model": True}}
    r= requests.post(HF_MODEL_URL, headers=HEADERS, json=payload)
    r.raise_for_status() # Raise an error for bad responses
    embs = r.json() # decodes the response object as JSON
    if isinstance(embs[0], float):
        embs = [embs]
    arr = np.array(embs, dtype=np.float32) #np.float32 reduces memory rather than np.float64
    return l2_normalize(arr)

def l2_normalize(arr):
    """L2 normalize a numpy array."""
    # axis=1 -> normalize horizontally (each row independently)
    # keepdims=True -> maintain the original number of dimensions
    norms= np.lialg.norm(arr, axis=1, keepdims=True) + 1e-12 # avoid division by zero (EPSILON)
    return arr / norms

def as_query(q: str) -> str:
    """Convert a query string to a format suitable for embedding."""
    return f"Represent this query for retrieving relevant documents: {q}"
