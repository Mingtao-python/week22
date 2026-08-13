from flask import Flask, request, render_template
from sentence_transformers import SentenceTransformer
import numpy as np

class RAG:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.docs = []
        self.chunks = []
        self.ids = []
        self.vecs = None

    def chunk(self, text, doc_id, size=200):
        for i in range(0, len(text), size):
            c = text[i:i+size]
            cid = len(self.chunks)
            self.chunks.append(c)
            self.ids.append((doc_id, cid, i))

    def add(self, docs):
        start = len(self.docs)
        self.docs.extend(docs)
        for i, d in enumerate(docs):
            self.chunk(d, start + i)
        v = self.model.encode(self.chunks)
        self.vecs = v if self.vecs is None else np.vstack([self.vecs, v])

    def search(self, q, k=3):
        qv = self.model.encode([q])[0]
        scores = np.dot(self.vecs, qv)
        idx = np.argsort(scores)[::-1][:k]
        out = []
        for i in idx:
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
        ctx = "\n".join([x["text"] for x in r])
        cit = "\n".join([
            f"[Doc {x['doc_id']} | Chunk {x['chunk_id']} | Offset {x['offset']}] Score={x['score']:.4f}"
            for x in r
        ])
        prompt = f"Context:\n{ctx}\n\nSources:\n{cit}\n\nQuestion: {q}\nAnswer:"
        ans = "(Fake LLM)\n" + prompt
        return ans, cit, ctx


app = Flask(__name__)
rag = RAG()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        docs = request.form.get("docs", "")
        query = request.form.get("query", "")
        if docs:
            rag.add([docs])
        if query:
            ans, cit, ctx = rag.answer(query)
            return render_template("index.html", answer=ans, citations=cit, context=ctx)
    return render_template("index.html", answer="", citations="", context="")

if __name__ == "__main__":
    app.run(debug=True)
