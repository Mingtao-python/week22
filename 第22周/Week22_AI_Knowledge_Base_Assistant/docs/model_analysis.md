# Model Analysis

## Retrieval method

The system uses SentenceTransformer Embedding, not TF-IDF.

## Generation mode

This environment does not provide a live external LLM backend, so the system is documented as a Retrieval-only prototype.

## Model details

- Model: sentence-transformers/all-MiniLM-L6-v2
- Embedding dimension: 384
- Retrieval method: SentenceTransformer Embedding
- Normalized cosine similarity is used for ranking

## Why this choice

- Real semantic retrieval is supported
- The product reflects actual embedding-based indexing and retrieval
- Output is consistent with the implementation and avoids unsupported claims

## Measurement notes

The project includes retrieval timing logic and uses high-level latencies recorded via `time.perf_counter()` in the retrieval pipeline. The values can be reported as average and variability over multiple runs.
