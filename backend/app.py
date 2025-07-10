from fastapi import Fastapi
from backend.router import router



app= Fastapi()
app.include_router(router)


@app.get("/")
def root():
    return {"message": "RAG Banking Assistant is up"}
            



