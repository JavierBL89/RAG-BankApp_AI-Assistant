from utils.json_file_saver import save_json_file
from typing import List, Dict
import json
from playwright.async_api import async_playwright



async def extract_by_sections_to_json(page):
    """
    Extracts sections from a webpage and returns them as a list of dictionaries.
    """
    print("Extacting sections from page...")

    sections = []
    headings = await page.query_selector_all("h1, h2, h3")  # fixed: correct selector syntax

    for heading in headings:
        title = (await heading.inner_text()).strip()
        sibling = await heading.evaluate_handle("node => node.nextElementSibling")
        content_parts = []

        while sibling:
              # check if sibling is null (JSHandle to null in Python)
            try:
                tag_name = await sibling.evaluate("node => node?.tagName")
            except Exception:
                break  # sibling was likely null

            tag_name = await sibling.evaluate("node => node?.tagName")
            if tag_name not in ["P", "UL", "OL"]:
                break
            text = await sibling.inner_text()
            content_parts.append(text.strip())
            sibling = await sibling.evaluate_handle("node => node.nextElementSibling")

        if content_parts:
            sections.append({
                "section_title": title,
                "content": " ".join(content_parts)
            })

    return sections


async def scrape_multiple_urls(url_list):
    
    print("Starting scraping process...")
    print(f"URLs to scrape: {url_list}")
    all_data = []
    print("Cretaing context.")
    async with async_playwright() as p:  # opens a Playwright context
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        for url in url_list:
            print(f"Scraping {url}")
            try:
                url.replace("'", "")
                page = await context.new_page()
                await page.goto(url, timeout=60000)
                await page.wait_for_load_state("networkidle")
                data = await extract_by_sections_to_json(page)
                all_data.append({"url": url, "sections": data})
                # Save the data to a JSON file
                await save_json_file(url, page, data)

                await page.close()
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        
        await browser.close()

    return all_data