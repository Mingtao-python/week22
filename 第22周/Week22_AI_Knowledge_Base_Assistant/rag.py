from typing import Any, Dict, List, Optional

from citation import build_citation, validate_answer_support
from retrieval import RetrievalEngine
from security.permissions import can_access_document


class KnowledgeBaseRAG:
    def __init__(self):
        self.db = RetrievalEngine().db
        self.retrieval_engine = RetrievalEngine(self.db)
        self.documents: List[str] = []
        self.hashes = set()
        self.retrieval_method = self.retrieval_engine.retrieval_method
        self.generation_mode = "Retrieval-only prototype"

    def add_documents(self, documents: List[str], metadata: Optional[List[Dict[str, Any]]] = None):
        self.db.add_documents(documents, metadata or [{} for _ in documents])
        self.documents.extend(documents)

    def answer(self, question: str, user_role: str = "student", top_k: int = 5):
        if not question or not question.strip():
            return {
                "answer": "No question was provided.",
                "sources": [],
                "citations": [],
                "retrieval_method": self.retrieval_method,
                "generation_mode": self.generation_mode,
            }

        search_response = self.retrieval_engine.search_with_timing(question, top_k=top_k, user_role=user_role, repeats=3)
        retrieved = search_response["results"]
        if not retrieved:
            return {
                "answer": "No relevant context was found for this question under the current role permissions.",
                "sources": [],
                "citations": [],
                "retrieval_method": self.retrieval_method,
                "generation_mode": self.generation_mode,
            }

        context = "\n\n".join(item["text"] for item in retrieved)
        system_prompt = (
            "You are a careful knowledge-base assistant. Answer using only the provided context, "
            "and include citations in the response. If the context is insufficient, say so explicitly."
        )
        user_prompt = (
            f"Question: {question}\n\nContext:\n{context}\n\n"
            "Provide a concise answer grounded in the context. Include citations using the exact source metadata."
        )

        answer_text = (
            f"Retrieval-only prototype: based on the retrieved context, the answer is grounded in {len(retrieved)} relevant chunks. "
            f"This environment does not provide an external LLM backend; the response is therefore retrieval-based and citation-grounded."
        )
        citations = []
        sources = []
        for item in retrieved:
            metadata = item.get("metadata", {})
            if can_access_document(user_role, metadata):
                chunk = {
                    "document_id": metadata.get("document_id", "unknown"),
                    "filename": metadata.get("filename", "unknown"),
                    "page": metadata.get("page", 1),
                    "chunk_id": metadata.get("chunk_id", "unknown"),
                    "text": item.get("text", ""),
                }
                citations.append(build_citation(chunk))
                sources.append({
                    "text": item.get("text", ""),
                    "metadata": metadata,
                    "citation": build_citation(chunk),
                })

        if not validate_answer_support(answer_text, sources):
            answer_text = "The retrieved context is insufficient to support a confident answer. Please upload more relevant material or rephrase the question."

        return {
            "answer": answer_text,
            "sources": sources,
            "citations": citations,
            "retrieval_method": self.retrieval_method,
            "generation_mode": self.generation_mode,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
        }
