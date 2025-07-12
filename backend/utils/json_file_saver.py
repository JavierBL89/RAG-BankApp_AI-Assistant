import os
import json
import re


def sanitize_filename(name: str) -> str:
    """Sanitize title to be a valid filename."""
    name = re.sub(r'[^\w\s-]', '', name)         # Remove special characters
    name = re.sub(r'\s+', '_', name.strip())     # Replace spaces with underscores
    return name[:50]                             # Limit length

def save_json_file(data:dict, title:str, folder: str = "scraped_pages"):
    """
    Save a dictionary as a JSON file in the given folder.
    If a file with the same name exists, append a number.
    """
    os.makedirs(folder, exist_ok=True)

    base_filename = sanitize_filename(title)
    filename = f'{base_filename}.json'
    path = os.path.join(folder, filename)
    
    # check for liked file names
    counter=1
    while os.path.exists(path):
        filename=f'{base_filename}_{counter}'
        path=os.path.join(folder,filename)
        counter +=1
    
    #save file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved to {path}")