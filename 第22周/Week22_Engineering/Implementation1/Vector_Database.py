import numpy as np
from sentence_transformers import SentenceTransformer

class MiniVectorDB:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.texts = []
        self.vectors = []

    def add_documents(self, docs):
        self.texts.extend(docs)
        embeddings = self.model.encode(docs)
        self.vectors.extend(embeddings)

    def search(self, query, top_k=5):
        q_vec = self.model.encode([query])[0]
        scores = np.dot(self.vectors, q_vec)
        idx = np.argsort(scores)[::-1][:top_k]
        return [(self.texts[i], float(scores[i])) for i in idx]


if __name__ == "__main__":
    db = MiniVectorDB()
    docs = [f"Sample text number {i}" for i in range(50)]
    db.add_documents(docs)

    result = db.search("sample", top_k=5)
    for r in result:
        print(r)
