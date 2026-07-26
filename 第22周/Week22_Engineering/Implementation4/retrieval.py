import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticRetrieval:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.texts = []
        self.vectors = []

    def add(self, docs):
        self.texts.extend(docs)
        vecs = self.model.encode(docs)
        self.vectors.extend(vecs)

    def search(self, query, top_k=5):
        q_vec = self.model.encode([query])[0]
        scores = np.dot(self.vectors, q_vec)
        idx = np.argsort(scores)[::-1][:top_k]
        return [(self.texts[i], float(scores[i])) for i in idx]


if __name__ == "__main__":
    docs = ["learn python", "python tutorial", "best python course", "java basics", "how to cook", "how to learn english"]
    engine = SemanticRetrieval()
    engine.add(docs)

    print(engine.search("how to learn python", top_k=3))
