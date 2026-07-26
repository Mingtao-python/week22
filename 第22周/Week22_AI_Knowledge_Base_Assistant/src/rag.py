from vector_database import VectorDatabase
from validation import prompt_filter, check_permission

def fake_llm(prompt: str) -> str:
    return "This is a demo answer based on the provided context."

class MiniRAGSystem:
    def __init__(self):
        self.db = VectorDatabase()

    def add_docs(self, docs, metas=None):
        self.db.add_documents(docs, metas)

    def answer(self, question: str, user_role: str = "student", top_k: int = 3):
        if not prompt_filter(question):
            return {"answer": "Prompt blocked by filter.", "sources": []}

        results = self.db.search(question, top_k=top_k)
        filtered = []
        for r in results:
            if check_permission(user_role, r["metadata"]):
                filtered.append(r)

        context = "\n".join([r["text"] for r in filtered])
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        ans = fake_llm(prompt)

        sources = [{"text": r["text"], "metadata": r["metadata"]} for r in filtered]
        return {"answer": ans, "sources": sources}