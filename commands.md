🚀 To Run It

### Terminal 1: Backend
cd backend
uvicorn main:app --reload

### Terminal 2: Frontend (optional, use Python or Node to serve static files)
cd frontend
python3 -m http.server 8080






list ports in used
 - lsof -i :7860

kill port
 - kill -9 <port>


1. Ensure you're in a virtual environment. If you haven't created one, create it:
   bash

    - python3.10 -m venv venv   (VERSION 10 NEEDED, not 13)

2. Activate the virtual environment:

    - source venv/bin/activate

   
5. Install Flask and all other required packages.
Verify Installation:
Check if Flask is installed:

- pip show flask

- pip install flask


6. Install Langchain:

   - pip install langchain-core langchain-community langchain
   

7. Install Dependencies from requirements.txt:
   Install all the dependencies listed in your requirements.txt file:

   - pip freeze > requirements.txt

   - pip install -r requirements.txt



8. Install Promptoo[embeddings]

- pip install "promptfoo[embedding]"


9. Install Langchain Communiity

- pip install langchain-community



10. Run Chroma(from root directory) to load datasource after changes in data

- python -m backend.data.index.chroma_index