from fastapi import APIRouter, Request
from rag_engine import handle_query


router = APIRouter()

@router.post("/chat")
async def chat(request:Request):
    body = await request.json()
    user_query = body.get("query")
    response = handle_query(user_query)
    return {"response": response}
