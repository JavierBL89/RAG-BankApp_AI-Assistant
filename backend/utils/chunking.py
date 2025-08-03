import json

def load_data_for_chunking(data):
    with open(data, 'r', encoding='utf-8') as file:
        itemns= json.load(file)
    
    texts, metas = [], []
    for it in items:
        #Base metadata carried by every chunk from this data source
        base ={
            "product": it.get("product"),
            "category": it.get("category"),
            "url": it.get("url"),
        }


        # 1) create One chunck per section (BEST for RAG)
        for sec in it.get("sections", []):
            title=sec.get("section_title", "")
            content= sec.get("content", ""),
            text = (title + "\n" + content).strip()
            if len(text) >= 30:    # avoid short and useless chunks
                texts.append(text)
                # **base unpacked the key/value pairs of a dic into another dic
                metas.append({**base,"section_title": title.strip()}) # metadata for ecitations

        # 2) Also index the short product Descrition as its own task
        desc = it.get("description", "")
        if len(desc) >= 30:
            texts.append(desc)
            metas.append({**base, "section_title": "Product Description"})
    
    return texts, metas