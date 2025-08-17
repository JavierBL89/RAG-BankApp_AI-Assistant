✅ Completed Components
🧠 1. Embedding
Model: BAAI/bge-m3
Function: Converts all documents (chunked sections + descriptions) into dense vectors.
Tooling: LangChain + HuggingFaceEmbeddings

🧩 2. Vector Store
Database: Chroma
Storage: Persistent local DB (persist_directory)
Metadata: Includes category, product, url, etc.
Status: Up and running, filterable!

🗣️ 3. Intent Recognition
Model: Mukalingam0813/multilingual-Distilbert-intent-classification (or similar)
Goal: Extract high-level intents as metadata → {category: ..., product: ...}
Next: Optional fine-tuning if needed for accuracy.
🧲 4. Context Retriever
Mechanism: Uses Chroma filtered retriever
Based on: Intent classifier output
Search type: Similarity search (k=5), filtered by category/product

📝 What’s Left
💬 5. Generator (LLM)
Goal: Generate a helpful, context-aware response using the retrieved chunks

Options:

Hugging Face Hosted API (e.g., mistral, zephyr, llama3, etc.)
OpenAI (gpt-3.5 / gpt-4) if available
Local model via transformers if resource permits
Integration: Use LangChain's LLMChain, StuffDocumentsChain, or custom prompt template