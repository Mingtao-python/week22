# Week22 AI Knowledge Base Assistant

This project is a product-oriented knowledge base assistant that supports uploading PDF, TXT, and Markdown documents, chunking them, embedding them with a real sentence-transformers model, indexing them in a vector database, and answering questions with citations and role-aware access control.

## Product goals

- Real document upload validation for PDF, TXT, and Markdown
- Real chunking pipeline with chunk size and overlap configuration
- Real embedding-based retrieval using SentenceTransformer
- Secure role-based filtering before retrieval
- Citation metadata including source file, page, and chunk id
- Web interface for upload and Q&A
- Test coverage for core product requirements

## Retrieval mode

- Retrieval method: SentenceTransformer Embedding
- Generation mode: Retrieval-only prototype

This project does not claim to be a general-purpose external LLM integration. It uses embedding-based retrieval and citations, and the response path is designed to require grounded evidence in the current environment.

## Structure

- app.py
- upload.py
- chunker.py
- embedding.py
- vector_database.py
- retrieval.py
- rag.py
- citation.py
- security/
- templates/
- tests/
- docs/
- data/
- requirements.txt

## Quick start

```bash
cd /workspaces/week22/第22周/Week22_AI_Knowledge_Base_Assistant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 and upload a document.
