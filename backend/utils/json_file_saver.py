import os
import json
import re
from urllib.parse import urlparse


def sanitize_filename(name: str) -> str:
    """Sanitize title to be a valid filename."""
    name = re.sub(r'[^\w\s\-&|]', '', name)           # Allow alphanumerics, space, -, &, |
    name = re.sub(r'[\s\-&|]+', '_', name.strip())    # Replace -, &, |, and whitespace with "_"
    return name[:50]                                  # Truncate to 50 chars


async def save_json_file(url, page: str, data: dict, folder: str = "scraped_pages"):
    """
    Save a dictionary as a JSON file in the given folder.
    If a file with the same name exists, append a number.
    """
    try:
        os.makedirs(folder, exist_ok=True)
        
        print("Saving data to JSON file...")
        base_filename = await get_page_title_or_hostname(url, page)

        print("Base filename:", base_filename)
        filename = f'{base_filename}.json'
        path = os.path.join(folder, filename)
        

        while os.path.exists(path):
            filename=f'{base_filename}.json'
            path=os.path.join(folder,filename)
        
        #save file
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
       
        print(f"Saved to {path}")

    except Exception as e:
        print(f"Error saving file: {e}")
        return None
    

async def get_page_title_or_hostname(url:str, page) -> str:
    try:
        title = await page.title()
        title = title.replace('|', '_')               # Replace '|' with '_'
        title = title.replace(' ', '')                # Remove all whitespaces
        title = re.sub(r'[^\w.-]', '', title)      
        return title
    except:
        clean_url = sanitize_filename(url)
        return urlparse(clean_url).hostname.replace(".", "_")