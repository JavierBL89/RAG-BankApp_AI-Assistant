from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import sys

from fastapi.middleware.cors import CORSMiddleware

from router import router  # adjust path if needed
# Add CORS middleware if frontend is on a different port (e.g. 3000)
from fastapi.responses import FileResponse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

origins = [
    "http://localhost:5500/",
    "http://127.0.0.1:5500/",
    "http://localhost:8000/",
    "http://127.0.0.1:8000/",
    "http://localhost:8080/",
    "http://127.0.0.1:8080/",
    "https://rag-bankapp-ai-assistant.onrender.com/",
    "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

# 👇 Mount the static directory
# Resolve absolute path to frontend/static
static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Root endpoint to check if the server is running
# 👇 Serve the index.html file at root
@app.get("/")
def root():
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html'))
    return FileResponse(html_path)
