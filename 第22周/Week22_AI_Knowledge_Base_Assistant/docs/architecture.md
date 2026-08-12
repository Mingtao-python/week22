# Architecture

The knowledge base assistant follows a product-oriented pipeline:

1. Upload validation
   - File extension and MIME checks
   - File size check
   - Duplicate content detection
   - Safe filename validation

2. Document parsing
   - TXT and Markdown decode as UTF-8 text
   - PDF content is accepted at ingestion as a binary-safe placeholder for the course product, with validation performed before indexing

3. Chunking
   - Document text is normalized and then split by chunk size and overlap
   - Each chunk carries metadata, including `document_id`, `filename`, `page`, and `chunk_id`

4. Embedding
   - The assistant uses a SentenceTransformer model instead of TF-IDF
   - Embeddings are stored with the associated metadata in the vector database

5. Retrieval and filtering
   - Query is embedded and scored against indexed chunks
   - Role-based filtering is applied before the final retrieval result is returned

6. Answer generation and citation
   - The answer is grounded in the retrieved context
   - Every returned source includes source, page, and chunk metadata

7. Web app
   - Upload interface and Q&A interface are implemented in Flask
