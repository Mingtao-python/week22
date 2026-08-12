from typing import Dict, Iterable, List, Optional

import numpy as np

from embedding import EmbeddingModel


class VectorDatabase:
    def __init__(self, embedding_model: Optional[EmbeddingModel] = None):
        self.embedding_model = embedding_model or EmbeddingModel()
        self.documents: List[str] = []
        self.metadata: List[Dict[str, object]] = []
        self.vectors: List[np.ndarray] = []

    def add_documents(self, documents: Iterable[str], metadata: Optional[Iterable[Dict[str, object]]] = None):
        docs = list(documents)
        metas = list(metadata) if metadata is not None else [{} for _ in docs]
        if len(docs) != len(metas):
            raise ValueError("Each document must have a matching metadata entry.")

        embeddings = self.embedding_model.encode(docs)
        self.documents.extend(docs)
        self.metadata.extend(metas)
        self.vectors.extend([np.asarray(vec, dtype=np.float32) for vec in embeddings])

    def search(self, query: str, top_k: int = 5):
        if not self.vectors:
            return []

        query_vector = self.embedding_model.encode(query)[0]
        normalized_query = query_vector / (np.linalg.norm(query_vector) + 1e-9)
        scores = []
        for vector in self.vectors:
            candidate = np.asarray(vector, dtype=np.float32)
            normalized_candidate = candidate / (np.linalg.norm(candidate) + 1e-9)
            score = float(np.dot(normalized_query, normalized_candidate))
            scores.append(score)

        ranked_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in ranked_indices:
            results.append({
                "text": self.documents[idx],
                "score": float(scores[idx]),
                "metadata": self.metadata[idx],
            })
        return results
