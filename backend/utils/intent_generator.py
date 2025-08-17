import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into os.environimport requests
import traceback

def generate_query_intent(text: str) :
    """
    Genreate different queries based on given the user query using a Mistral-instruct-7b model.
    
    Args:
        text (str): The input text to classify.
        
    Returns:
        List: Generated intent queries.
    """
    if text is None or text.strip() == "":
        return "Sorry, no input text provided."
    
    custom_message= "❌ Sorry, Model is unavailable."
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    # text = "What is the interest rate for savings accounts?"
    try:
        headers = {
        "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
        "Content-Type": "application/json"
        }
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": 
                       "You are a helpful assistant. Your task is to generate 2 variations of a given user query that preserve the original meaning but use different wording.\n"
                        "Respond only with a list of 2 rephrased queries. Do not include any explanation.\n"
                        "For example, if the user query is 'What is the interest rate for savings accounts?', you might respond with:\n"
                        "- What are the interest rates for savings accounts?\n"
                        "- How much interest do savings accounts offer?\n"
                        "- What is the current interest rate for savings accounts?\n"

                        "## User Query"
                        "User query:" + text
                }
            ],
            "model": "meta-llama/Meta-Llama-3-8B-Instruct:novita",
        }
        response = requests.post(API_URL, headers=headers, json=payload)

        # parse results
        if response.status_code == 200:
            result = response.json()
            print("✅ Response:", result["choices"][0]["message"]["content"])
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            traceback.print_exc()
            return custom_message
        
    except Exception as e:
        print(f"Error generating query intent: {e}")
        traceback.print_exc()
        return custom_message
        


