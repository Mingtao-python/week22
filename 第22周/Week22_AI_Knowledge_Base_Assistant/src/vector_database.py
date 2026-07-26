import numpy as np
from sentence_transformers import SentenceTransformer

class VectorDatabase:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.texts = []
        self.metadata = []
        self.vectors = []

    def add_documents(self, docs, metas=None):
        if metas is None:
            metas = [{} for _ in docs]
        self.texts.extend(docs)
        self.metadata.extend(metas)
        embeddings = self.model.encode(docs)
        self.vectors.extend(embeddings)

    def search(self, query, top_k=5):
        q_vec = self.model.encode([query])[0]
        scores = np.dot(self.vectors, q_vec)
        idx = np.argsort(scores)[::-1][:top_k]
        results = []
        for i in idx:
            results.append({
                "text": self.texts[i],
                "score": float(scores[i]),
                "metadata": self.metadata[i]
            })
        return results