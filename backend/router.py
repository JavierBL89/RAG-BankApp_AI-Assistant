from fastapi import APIRouter, Request
import json
#from rag_engine import handle_query
from utils.scraper import scrape_multiple_urls
router = APIRouter()
from typing import List
from pydantic import BaseModel

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