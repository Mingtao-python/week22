import numpy as np
from sentence_transformers import SentenceTransformer

def test_accuracy(docs, query, chunk_size, top_k):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunks = [docs[i:i+chunk_size] for i in range(0, len(docs), chunk_size)]
    chunks = [" ".join(c) for c in chunks]

    vecs = model.encode(chunks)
    q_vec = model.encode([query])[0]

    scores = np.dot(vecs, q_vec)
    idx = np.argsort(scores)[::-1][:top_k]
    return idx[0]

if __name__ == "__main__":
    docs = ["Python is great"] * 1000
    query = "python"

    for size in [100, 300, 500]:
        print("Chunk:", size, "Result:", test_accuracy(docs, query, size, 3))
