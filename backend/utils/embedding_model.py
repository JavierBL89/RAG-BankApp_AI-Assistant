import os
import pickle

# Define path to your local model file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "models", "minilm_model.pkl"))

def load_local_embeddings():
    """
    Loads the pre-trained sentence-transformer embeddings model from a local file.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"❌ Embedding model not found at: {MODEL_PATH}")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    
    print(f"✅ Loaded local embedding model from: {MODEL_PATH}")
    return model

# Expose global instance
embeddings = load_local_embeddings()
