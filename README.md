# **Banking Chatbot with Retrieval-Augmented Generation (RAG)**

This project is a **Banking Chatbot** designed to assist users in exploring financial products such as mortgages, loans, credit cards, savings, and pensions. The chatbot uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware responses by retrieving information from a curated knowledge base.

---

## **Features**
- **Instant Answers**: Provides quick and accurate answers to user queries about banking products.
- **Knowledge Base**: Covers a wide range of financial products, including:
  - Mortgages: First-Time Buyer, Home Mover, Buy-to-Let
  - Loans: Personal, Car, Student
  - Credit Cards: Classic, Platinum, Student
  - Accounts: Graduate, Basic, Smart Start
  - Savings: SuperSaver, Save for Kids
  - Pensions: Retirement, Company, Calculators
- **Query Examples**:
  - "How much can I borrow for my first home?"
  - "What’s the difference between a personal loan and a car loan?"
  - "Am I eligible for a Smart Start Account for my child?"
- **Powered By**:
  - **LangChain + FastAPI** for backend logic.
  - **Hugging Face Inference API** for embeddings.
  - **Chroma Vector Store** for vector-based search.
  - **Meta-Llama-3-8B-Instruct** for response generation.

---

## **How It Works**
1. **User Query**: The user submits a query through the chatbot interface.
2. **Embedding Generation**: The query is sent to a Hugging Face Space for embedding generation.
3. **Vector Search**: The embedding is used to search the Chroma Vector Store for relevant documents.
4. **Response Generation**: The retrieved documents are used to generate a context-aware response.

---

## **Project Structure**
```
.
├── backend/
│   ├── main.py                # FastAPI backend
│   ├── search_chroma.py       # Handles vector search and retrieval
│   ├── embedding_model.py     # Embedding generation using Hugging Face Space
│   └── utils/
│       ├── embeddings_hf.py   # Hugging Face embedding utilities
│       └── chunking.py        # Document chunking logic
├── frontend/
│   ├── index.html             # Chatbot UI
│   ├── static/
│       ├── css/
│       │   └── style.css      # Frontend styling
│       ├── js/
│       │   └── app.js         # Frontend logic
│       └── images/            # Icons and images
├── data/
│   └── index/                 # Chroma vector store persistence
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/banking-chatbot.git
cd banking-chatbot
```

### **2. Install Dependencies**
Ensure you have Python 3.8+ installed. Install the required Python packages:
```bash
pip install -r requirements.txt
```

### **3. Run the Backend**
Start the FastAPI backend:
```bash
uvicorn backend.main:app --reload
```

### **4. Serve the Frontend**
Open the 

index.html

 file in your browser or use a local server (e.g., Live Server in VS Code).

---

## **Usage**
1. Open the chatbot interface in your browser.
2. Ask questions about banking products (e.g., "What are the fees for a Graduate Current Account?").
3. View the chatbot's response, which is generated using the RAG pipeline.

---

## **API Endpoints**
- **Root Endpoint**: Serves the frontend:
  ```
  GET /
  ```
- **Static Files**: Serves static assets like JavaScript and CSS:
  ```
  GET /static/<file>
  ```
- **Embedding API**: Uses Hugging Face Space for embedding generation:
  ```
  POST /api/embed
  ```

---

## **Technologies Used**
- **Backend**:
  - [FastAPI](https://fastapi.tiangolo.com/): High-performance web framework.
  - [LangChain](https://langchain.com/): Framework for building LLM-powered applications.
  - [Chroma](https://www.trychroma.com/): Vector database for semantic search.
- **Frontend**:
  - HTML, CSS, JavaScript.
- **Machine Learning**:
  - Hugging Face Inference API for embeddings.
  - Meta-Llama-3-8B-Instruct for response generation.

---

## **Troubleshooting**

### **CORS Issues**
If you encounter CORS errors when running the app locally:
1. Ensure the frontend and backend are running on the same origin or add the frontend's URL to the `allow_origins` list in `main.py`.

### **Hugging Face Space Not Found**
If the Hugging Face Space URL is not reachable:
1. Verify the Space URL and ensure it is running.
2. Check the `/embed` endpoint for proper configuration.

---

## **Future Improvements**
- Add user authentication for personalized responses.
- Expand the knowledge base to include more financial products.
- Integrate a feedback mechanism for users to rate responses.

---

## **Contributing**
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.
