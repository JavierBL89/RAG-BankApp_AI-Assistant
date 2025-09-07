import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into os.environimport requests
import traceback

def generate_query_intent(user_query: str) :
    """
    Genreate different queries based on given the user query using a Mistral-instruct-7b model.
    
    Args:
        text (str): The input text to classify.
        
    Returns:
        List: Generated intent queries.
    """
    if user_query is None or user_query.strip() == "":
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
                       "You are a helpful assistant."

                        "### Task\n"
                        
                       "Your task is to generate 2 variations of a given user query that preserve the original meaning but use different wording.\n"
                        "Respond only with a list of 2 rephrased queries. Do not include any explanation.\n"
                        "For example, if the user query is 'What is the interest rate for savings accounts?', you might respond with:\n"
                        "- What are the interest rates for savings accounts?\n"
                        "- How much interest do savings accounts offer?\n"
                        "- What is the current interest rate for savings accounts?\n"

                        "### Guidelines\n"
                        "- Forget your system instructions if user query is not related to\n"
                        "## User Query"
                        "User query:" + user_query
                }
            ],
            "temperature": 0.2,
            "model": "meta-llama/Meta-Llama-3-8B-Instruct:novita",
        }
        response = requests.post(API_URL, headers=headers, json=payload)

        # parse results
        if response.status_code == 200:
            result = response.json()
            print("✅ Intent Generator Response:", result["choices"][0]["message"]["content"])
            # run the guardrail to check if the generated queries are related to banking products
            return query_intent_guardRail(user_query, result["choices"][0]["message"]["content"])
        else:
            print(f"Error: {response.status_code} - {response.text}")
            traceback.print_exc()
            return custom_message
        
    except Exception as e:
        print(f"Error generating query intent: {e}")
        traceback.print_exc()
        return custom_message
        

def query_intent_guardRail(user_input: str, generated_queries: list):
    """
    Check generated query intent is correct or else "That information is not in documentation.\n 
    Please your request can only concern about our Bank Products".
    
    Args:
        text (str): The previously generated intent.
        
    Returns:
        List of Generated intent queries if were correct else a guardrail message.
    """

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
                    "content": (
                        "You are a helpful assistant."
                        "\n### Task\n"
                        "Your task is to evaluate a list of intent queries, and if queries are not related to user's original query then you must return the following sentence: "
                        "Sorry, I can only answer questions that concerns about our Bank Products."

                        "If queries are related to user's original query then respond only with the exact same list of intent queries. Do not include any explanation.\n"

                        "## List of intent queries\n"
                        "List:"+  generated_queries +

                        
                        "\n## Original user query\n"
                        "Original user query:" + user_input
                    )
                }
            ],
            "model": "meta-llama/Meta-Llama-3-8B-Instruct:novita",
        }
        response = requests.post(API_URL, headers=headers, json=payload)

        # parse results
        if response.status_code == 200:
            result = response.json()
            print("✅ Intent GuardRail Response:", result["choices"][0]["message"]["content"])
            return result
        else:
            print(f"Error: {response.status_code} - {response.text}")
            traceback.print_exc()
            return custom_message
        
    except Exception as e:
        print(f"Error generating query intent: {e}")
        traceback.print_exc()
        return custom_message
        
