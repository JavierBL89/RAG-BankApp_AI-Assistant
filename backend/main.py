from fastapi import FastAPI
from router import router



app = FastAPI()
app.include_router(router)


@app.get("/")
def root():
    return {"message": "RAG Banking Assistant is up"}
            



