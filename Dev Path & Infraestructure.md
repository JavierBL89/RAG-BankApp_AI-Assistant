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

**Multilingual Models Options**
| Model                                                        | Size             | Notes                                                                             |
| ------------------------------------------------------------ | ---------------- | --------------------------------------------------------------------------------- |
| `BAAI/bge-m3`                                                | Large (1.8GB)    | Strong multilingual, supports dense + sparse retrieval. Great quality but slower. |
| `paraphrase-multilingual-MiniLM-L12-v2`                      | Medium (\~400MB) | Good multilingual baseline, much faster.                                          |
| `sentence-transformers/distiluse-base-multilingual-cased-v2` | Medium (\~480MB) | DistilUSE, decent cross-language matching, very fast.                             |


We selected ->`paraphrase-multilingual-MiniLM-L12-v2`  

**English-only – Best Accuracy**

| Model                        | Size    | Notes                                             |
| ---------------------------- | ------- | ------------------------------------------------- |
| `BAAI/bge-base-en-v1.5`      | \~400MB | Very strong retrieval performance for English.    |
| `BAAI/bge-large-en-v1.5`     | \~1.3GB | State-of-the-art accuracy, but heavier.           |
| `all-mpnet-base-v2`          | \~420MB | One of the best general-purpose ST models.        |
| `multi-qa-mpnet-base-dot-v1` | \~420MB | Fine-tuned for question-answer retrieval.         |
| `all-MiniLM-L6-v2`           | \~80MB  | Very fast, lower accuracy, great for prototyping. |

**Small / Lightweight Models (Fast, Low Memory)**

If speed and memory footprint are priority:

| Model                     | Size    | Notes                                |
| ------------------------- | ------- | ------------------------------------ |
| `all-MiniLM-L12-v2`       | \~120MB | Good balance of speed/quality.       |
| `all-MiniLM-L6-v2`        | \~80MB  | Very fast, low accuracy drop.        |
| `paraphrase-MiniLM-L6-v2` | \~80MB  | Great for sentence similarity tasks. |

**Domain-specific / Question-Answer Focused**

If the main use case is RAG-style Q&A:

| Model                          | Notes                                                                             |
| ------------------------------ | --------------------------------------------------------------------------------- |
| `multi-qa-MiniLM-L6-cos-v1`    | Fast, trained for QA retrieval.                                                   |
| `multi-qa-distilbert-cos-v1`   | Slightly bigger but QA-focused.                                                   |
| `nomic-ai/nomic-embed-text-v1` | Open-source alternative to OpenAI's `text-embedding-ada-002`, good for retrieval. |

BGE stands for BAAI General Embedding — a family of text embedding models released by the Beijing Academy of Artificial Intelligence (BAAI).

They’re designed for retrieval, semantic search, and RAG pipelines, and are competitive with or better than OpenAI’s text-embedding-ada-002 in many benchmarks — but completely open source.

### Key Points

**Specialization**
- Optimized for text retrieval tasks (e.g., search, question answering).
- Trained with contrastive learning on huge datasets so that relevant docs and queries align.

Family
- English: bge-small-en-v1.5, bge-base-en-v1.5, bge-large-en-v1.5
- Multilingual: bge-m3 (supports 100+ languages, including English and Spanish).
- Sizes: small (fast, ~384 dims), base (~768 dims), large (~1024 dims).

Instruction-tuned for queries
- For best results with retrieval, BGE expects a different prompt for queries and documents:

1. Documents: embed as-is.
2. Queries: prepend something like

´´´bash
Represent this query for retrieving relevant documents: {query}
´´´
This helps the model better align query intent with stored documents.

Performance
- On the MTEB benchmark (Massive Text Embedding Benchmark), bge-large-en-v1.5 and bge-m3 rank at or near the top among open models.
- Multilingual bge-m3 keeps strong performance even outside English.

Open Source
- License: Apache 2.0 → free for commercial use.
- Hosted on Hugging Face, can be run locally or via HF Inference API.



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