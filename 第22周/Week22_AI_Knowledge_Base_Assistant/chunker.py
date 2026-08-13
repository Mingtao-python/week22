import re
from typing import Dict, List, Optional


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_documents(text: str, size: int = 500, overlap: int = 0, document_id: Optional[str] = None, filename: Optional[str] = None, page_map: Optional[Dict[str, int]] = None):
    clean_text = normalize_text(text)
    if not clean_text:
        return []

    if size <= 0:
        raise ValueError("Chunk size must be positive.")
    step = max(1, size - overlap)
    chunks: List[Dict[str, object]] = []
    page_map = page_map or {"default": 1}

    for index in range(0, len(clean_text), step):
        piece = clean_text[index:index + size].strip()
        if not piece:
            continue
        page_number = page_map.get("default", 1)
        if page_map and "page" in page_map:
            page_number = page_map["page"]
        chunk_id = f"{document_id or 'chunk'}-{len(chunks) + 1:03d}"
        chunks.append({
            "chunk_id": chunk_id,
            "document_id": document_id,
            "filename": filename,
            "page": page_number,
            "text": piece,
        })

    return chunks
