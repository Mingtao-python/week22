def build_citation(chunk: dict) -> str:
    if not isinstance(chunk, dict):
        raise ValueError("Chunk must be a dictionary.")

    document_id = chunk.get("document_id", "unknown")
    filename = chunk.get("filename", "unknown")
    page = chunk.get("page", 1)
    chunk_id = chunk.get("chunk_id", "unknown")
    return (
        f"Source: {filename}\n"
        f"Document: {document_id}\n"
        f"Page: {page}\n"
        f"Chunk: {chunk_id}"
    )


def validate_answer_support(answer_text: str, sources: list) -> bool:
    if not answer_text or not sources:
        return False
    text = answer_text.lower()
    for source in sources:
        chunk_text = str(source.get("text", "")).lower()
        if chunk_text and any(token in text for token in [
            chunk_text[:20],
            source.get("filename", "").lower(),
        ]):
            return True
    return False
