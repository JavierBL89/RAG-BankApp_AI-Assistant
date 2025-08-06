from transformers import pipeline,AutoTokenizer,AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretreianed("Mukalingham0813/multilingual-Distilbert-intent-classification")
model = AutoModelForSequenceClassification.from_pretained("Mukalingham0813/multilingual-Distilbert-intent-classification")

intent_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def classify_intent(text: str) :
    """
    Classify the intent of a given text using a pre-trained model.
    
    Args:
        text (str): The input text to classify.
        
    Returns:
        str: The predicted intent label.
    """
    if not text.strip():
        return "unknown"
    
    result = intent_classifier(text, return_all_scores=False)
    print(f"Intent classification result: {result}")
    return result[0]["label"], float(result[0]["score"])

