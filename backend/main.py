from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from router import router  # adjust path if needed
# Add CORS middleware if frontend is on a different port (e.g. 3000)
from fastapi.responses import FileResponse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()


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
