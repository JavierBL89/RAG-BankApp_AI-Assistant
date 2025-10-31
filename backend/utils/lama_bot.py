import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into os.environimport requests
import traceback

async def generate_response(context: list, all_queries: list[str]) :
    """

    """
    print("Generating response based on context:", context)
    if context is None or context == []:
        return "Sorry, no context provided."
    
    ########## Use citations in your context
    ### Instead of injecting the whole text, you could:
    # 1. Extract just titles + snippets
    # 2. Add a placeholder like [doc1]: link-to-doc
    # 3.Let the model reference them, rather than read them all
    ######### Why this is a BEST approach???:
    # Shorter prompt = faster, cheaper, fewer token errors
    # Improves model accuracy by giving:
    # Clear structure (title, section)
    # Condensed information (first 300 characters)
    # Encourages citation-based responses instead of regurgitating full passages
    formatted_context = "\n\n".join([
        f"[{i+1}] **{doc.metadata.get('product', 'Unknown Product')}** "
        f"({doc.metadata.get('section_title', 'Unknown Section')}): "
        f"{doc.page_content[:300].strip()}...\n"
        f"🔗 {doc.metadata.get('url', 'No URL')}"
        for i, doc in enumerate(context)
    ])

    # Convert list to string
    merged_query = " ".join(all_queries)
    print(formatted_context)

    custom_message= "❌ Sorry, Model is unavailable."
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    # text = "What is the interest rate for savings accounts?"
    try:
        headers = {
        "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
        "Content-Type": "application/json"
        }
        payload = {
            
            "temperature": 0.3,
            "messages": [
                {
                    "role": "system",
                    "content": 
                    f"""
                       ### Role
                       You are a helpful assistant of a Banking application for the Bank of Ireland stricly.
                       
                       ### Format and Style
                       - Responde in a friendly and professional tone.
                       - Format your response in Markdown when apopropriate.

                       ### Response instructions
                       - Do not start your response with a headding about the topic.
                       - If the retrieved document is clearly related to the **user’s topic**, generate a concise and relevant answer using only that information.
                       - Do not invent information or provide answers that are not in the retrieved documents.
                       - Base your answer only on the provided context.
                       - Provide the relevant link in the document where the answer was found.
                       - If the user asks for a specific product, provide the link to that product.

                       ### Retrieved documents: {formatted_context}

                        ### User querys:
                        {merged_query}
                """
                }
            ],
            "model": "meta-llama/Meta-Llama-3-8B-Instruct:novita",
        }
        response = requests.post(API_URL, headers=headers, json=payload)

        # parse results
        if response.status_code == 200:
            result = response.json()
            print("✅ Response:", result["choices"][0]["message"]["content"])
            return result
        else:
            print(f"Error: {response.status_code} - {response.text}")
            traceback.print_exc()
            return custom_message
        
    except Exception as e:
        print(f"Error generating query intent: {e}")
        traceback.print_exc()
        return custom_message
        


