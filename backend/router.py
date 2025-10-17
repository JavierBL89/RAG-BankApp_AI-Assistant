from fastapi import APIRouter, HTTPException
import json
#from rag_engine import handle_query
from utils.scraper import scrape_multiple_urls
import os
from typing import List
from pydantic import BaseModel
from typing import Optional, Dict, Any
from utils.search_chroma import retrieve_similar_docs
from utils.intent_generator import generate_query_intent
from utils.lama_bot import generate_response
from itertools import chain
from fastapi.responses import FileResponse, JSONResponse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


router = APIRouter()

# Define the input model for the search query(deserialize)
class QueryInput(BaseModel):
    query:str
    k: int=5
    where: Optional[Dict[str, Any]] = None

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


@router.post("/chat")
async def chat(q:QueryInput):
    """
    Search the knowledge base with a query.
    """
    try:
        # 1. generate different query intents based on user query
        intent_output = generate_query_intent(q.query)
    except Exception as e:
        import traceback
        print("❌ CHAT ROUTE ERROR:", e)
        traceback.print_exc()
        return {"error": str(e)}
    
    raw_output = intent_output["choices"][0]["message"]["content"]
    # raw_output = intent_output["choices"][0]["message"]["content"]
    if "Sorry, I can only answer questions that concerns about our Bank Products" in raw_output:
         print("Generated output indicates:", raw_output)
         return intent_output

    print("Raw output from intent generator:", raw_output)
    raw_output = raw_output.replace("\n", "")
    raw_output = raw_output.replace("- ", "-")
    generated_queries = [q.strip() for q in raw_output.split("-") if q.strip()]
    generated_queries.append(q.query) # append the original query to the list of queries
    all_queries = generated_queries
    print("Generated queries:", all_queries)

    # 2. retrieve relevant documents based on the query
    try:
        relevant_docs = await retrieve_similar_docs(all_queries)
        print("Retrieved documents:", relevant_docs)
    except Exception as e:
        import traceback
        print("❌ ERROR retrieving docs:", e)
        traceback.print_exc()
        return {"error": f"Retriever failed: {e}"}
    
    # 3. generate response based on the retrieved documents and intent
    context = [doc.page_content for doc in relevant_docs] # extract only page content (no metadata) from retrieved documents
    print("Context for response generation:", context)
    bot_response = await generate_response(relevant_docs)

    return bot_response


@router.post("/generate_intent")
def generate_intent(q:QueryInput):
    """
    Search the knowledge base with a query.
    """
    return generate_query_intent(q.query)


# --- JSON FILES ---
BASE_DIR = "../../frontend/static"

# --- JSON FILES ---
@router.get("/download-json")
def download_json():
    json_path = os.path.join(BASE_DIR, "products.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="products.json not found")
    return FileResponse(json_path, media_type="application/json", filename="products.json")

@router.get("/view-json")
def view_json():
    json_path = os.path.join(BASE_DIR, "products.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="products.json not found")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return JSONResponse(content=data)


# --- IMAGES ---
@router.get("/view-image/{image_name}")
def view_image(image_name: str):
    image_path = os.path.join(BASE_DIR, "images", f"{image_name}.png")
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail=f"{image_name}.png not found")

    return FileResponse(image_path, media_type="image/png")

            