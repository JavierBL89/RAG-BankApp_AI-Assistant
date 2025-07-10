# 🧠 RAG Banking System Architecture

## 🧵 Framework
**Backend**: FastAPI
**Frontend / App**: Kotlin
**RAG Flow Orchestration**: LangChain (Python)



## 🔍 Scraping

- ✅ **Playwright** → Best for modern websites with JavaScript rendering.
- 🟡 **BeautifulSoup + requests** → Simpler, for static HTML pages.

## 📦 Embedding + Vector Storage

### Embeddings
- **sentence-transformer** `Hugging Face Transformers`

### Vector Stores
- **ChromaDB** – Lightweight, flexible, great for LangChain


## 🔍 Vector Search (Retrieval)

Use LangChain’s retriever:
```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

## 🧭 Intent Recognition / Routing

- **LangChain Router** - MultiPromptChain or RouterChain (works well for multi-intent chatbots)

- **Alternatives**

- Prompt-based classification (zero-shot) using GPT
- OpenAI function calling or Tool usage + descriptions