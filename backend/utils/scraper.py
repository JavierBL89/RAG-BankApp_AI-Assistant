from playwright.sync_api import sync_playwright
from typing import List, Dict
import json

def extract_by_tags_to_json(url: str, tags: List[str]) -> Dict[str, List[str]]:
    """
    Extracts text content by HTML tags and returns a JSON-style dictionary.

    Args:
        url (str): The webpage to scrape.
        tags (List[str]): Tags to extract (e.g., ['h1', 'p', 'li']).

    Returns:
        Dict[str, List[str]]: JSON-style dictionary with tag names as keys and list of texts as values.
        E.g
        {
            "h1": ["Welcome to Banking Portal"],
            "h2": ["Open an Account"],
            "p": ["Our banking services offer..."],
            "li": ["Savings Account", "Credit Card", "Loans"]
        }
    """

    results = {}

    with sync_playwright() as p:  # opens a Playwright context
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        for tag in tags:
            tag_texts= []
            elements = page.locator(tag)
            count = elements.count()
            for i in range(count):
                text = elements.nth(i).inner_text().strip()
                if text:
                    tag_texts.append(text)
            results[tag] = tag_texts

        browser.close()

    return results