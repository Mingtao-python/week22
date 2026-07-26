import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class FAISSRetrieval:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.texts = []

    def build(self, docs):
        self.texts = docs
        vectors = self.model.encode(docs)
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)

    def search(self, query, top_k=5):
        q_vec = self.model.encode([query])
        distances, idx = self.index.search(q_vec, top_k)
        return [(self.texts[i], float(distances[0][j])) for j, i in enumerate(idx[0])]


if __name__ == "__main__":
    docs = [f"FAISS document {i}" for i in range(50)]
    engine = FAISSRetrieval()
    engine.build(docs)

    print(engine.search("document", top_k=5))
