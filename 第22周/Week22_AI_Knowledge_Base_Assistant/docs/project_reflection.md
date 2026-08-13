# Project Reflection

This project moves from experimental implementations to a product-style architecture. The primary change is that every component is now aligned with the stated requirement: document ingestion, chunking, embedding, vector storage, retrieval, citation, and role-based access all exist in the same product structure.

The main lesson is that product truth must match reporting. If the pipeline uses sentence-transformers, then the interface must state `SentenceTransformer Embedding` rather than a misleading TF-IDF label. Similarly, if the implementation is retrieval-only, it must not be described as a full LLM-based RAG system.

The resulting structure is more realistic and more maintainable, and it better supports future extension to external LLM orchestration or calibrated evaluation datasets.
