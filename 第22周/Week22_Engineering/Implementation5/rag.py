import numpy as np
from sentence_transformers import SentenceTransformer

class FullRAG:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.docs = []
        self.chunks = []
        self.ids = []
        self.vecs = []

    def chunk(self, text, doc_id, size=200):
        for i in range(0, len(text), size):
            c = text[i:i+size]
            cid =len(self.chunks)
            self.chunks.append(c)
            self.ids.append((doc_id, cid, i))

    def add(self, docs):
        start = len(self.docs)
        self.docs.extend(docs)
        for i, d in enumerate(docs):
            self.chunk(d, start + i)
        new_vecs = self.model.encode(self.chunks[len(self.vecs):])
        self.vecs.extend(new_vecs)

    def search(self, q, k=3):
        if not self.vecs:
            return []
        qv = self.model.encode([q])[0]
        scores = np.dot(self.vecs, qv)
        idx = np.argsort(scores)[::-1][:k]
        out = []
        for i in idx:
            if i >= len(self.ids):
                continue
            doc_id, cid, off = self.ids[i]
            out.append({
                "doc_id": doc_id,
                "chunk_id": cid,
                "offset": off,
                "text": self.chunks[i],
                "score": float(scores[i])
            })
        return out

    def answer(self, q):
        r = self.search(q)
        if not r:
            return "No retrieval", "", ""
        ctx = "\n".join([x["text"] for x in r])
        cit = "\n".join([
            f"[Doc {x['doc_id']} | Chunk {x['chunk_id']} | Offset {x['offset']}] Score={x['score']:.4f}"
            for x in r
        ])
        prompt = f"Context:\n{ctx}\n\nSources:\n{cit}\n\nQuestion: {q}\nAnswer:"
        ans = "(Fake LLM)\n" + prompt
        return ans, cit, ctx




def fake_llm(prompt):
    return "(Fake LLM)\n" + prompt + "\nGenerated answer."


if __name__ == "__main__":
    rag = FullRAG(fake_llm)
    docs = [
        "Python is a programming language widely used for AI and data science.",
        "Java is commonly used for backend development and enterprise systems.",
        "Embeddings represent text as dense vectors for semantic search."
    ]
    rag.add_docs(docs)
    result = rag.answer("What is Python?")
    print(result["answer"])
    print(result["sources"])
