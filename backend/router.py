from fastapi import APIRouter, Request
import json
#from rag_engine import handle_query
from utils.scraper import scrape_multiple_urls
router = APIRouter()
from typing import List
from pydantic import BaseModel
from utils.embedding_model import embeddings
from langchain_community.vectorstores import Chroma
from typing import Optional, Dict, Any
from utils.search_chroma import get_retreivers
from utils.intent_generator import generate_query_intent

PERSIST_DIR = "data/index"
COLLECTION = "banking_rag"

# Define the input model for the search query(deserialize)
class QueryInput(BaseModel):
    query:str
    k: int=5
    where: Optional[Dict[str, Any]] = None


# @router.post("/chat")
# async def chat(request:Request):
#     body = await request.json()
#     user_query = body.get("query")
 #   response = handle_query(user_query)
    # return {"response": response}


class ScrapeRequest(BaseModel):
    scrape_url: List[str]

@router.post("/scrape")
async def scrape_web_content(request: ScrapeRequest):
    body = request.scrape_url
    print("Received URLs for scraping:", body)
    retrieved_json_dict = await scrape_multiple_urls(body)
    print("Sections retrieved:", retrieved_json_dict)

    return {"scraped_data": retrieved_json_dict}

## TRY AND START SCRAPING CONTENT, THEN COMMIT IMPL


@router.post("/search")
def search(q:QueryInput):
    """
    Search the knowledge base with a query.
    """
    # load indexed data from Chroma
    vs = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )
    # 1. generate different query intents
    intents = generate_query_intent(q.query)
    # 2. retrieve relevant documents based on the query
    retreived = get_retreivers(user_input=q.query, intent=intents)

    # 3. generate response based on the retrieved documents and intent

    #results
    return {"message": "Search functionality is not implemented yet."}

@router.post("/chat")
def search(q:QueryInput):
    """
    Search the knowledge base with a query.
    """
    return generate_query_intent(q.query)
            