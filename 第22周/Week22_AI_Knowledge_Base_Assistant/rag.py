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

    def answer(
        self,
        question: str,
        user_id: Optional[str] = None,
        user_role: str = "student",
        top_k: int = 5,
        permission_checker: Optional[Any] = None
    ):

        # 1. Empty question check
        if not question or not question.strip():
            return {
                "answer": "No question was provided.",
                "sources": [],
                "citations": [],
                "retrieval_method": self.retrieval_method,
                "generation_mode": self.generation_mode,
            }

        # 2. Perform retrieval
        search_response = self.retrieval_engine.search_with_timing(
            question,
            top_k=top_k,
            user_role=user_role,
            repeats=3
        )
        retrieved = search_response["results"]

        # 3. No results found
        if not retrieved:
            return {
                "answer": (
                    "No relevant context was found for this question under the current "
                    "role permissions."
                ),
                "sources": [],
                "citations": [],
                "retrieval_method": self.retrieval_method,
                "generation_mode": self.generation_mode,
            }

        # 4. Build context for generation
        context = "\n\n".join(item["text"] for item in retrieved)

        system_prompt = (
            "You are a careful knowledge-base assistant. Answer using only the provided "
            "context, and include citations in the response. If the context is insufficient, "
            "say so explicitly."
        )

        user_prompt = (
            f"Question: {question}\n\nContext:\n{context}\n\n"
            "Provide a concise answer grounded in the context. Include citations using "
            "the exact source metadata."
        )

        # 5. Retrieval-only fallback answer (no LLM backend)
        answer_text = (
            f"Retrieval-only prototype: based on the retrieved context, the answer is "
            f"grounded in {len(retrieved)} relevant chunks. This environment does not "
            f"provide an external LLM backend; the response is therefore retrieval-based "
            f"and citation-grounded."
        )

        # 6. Build citations + sources with permission checking
        citations = []
        sources = []

        for item in retrieved:
            metadata = item.get("metadata", {})

            # External permission checker (preferred)
            if permission_checker:
                allowed = permission_checker(metadata)
            else:
                # Fallback to built-in permission system
                allowed = can_access_document(user_role, metadata)

            if allowed:
                chunk = {
                    "document_id": metadata.get("document_id", "unknown"),
                    "filename": metadata.get("filename", "unknown"),
                    "page": metadata.get("page", 1),
                    "chunk_id": metadata.get("chunk_id", "unknown"),
                    "text": item.get("text", ""),
                }

                citation = build_citation(chunk)
                citations.append(citation)

                sources.append({
                    "text": item.get("text", ""),
                    "metadata": metadata,
                    "citation": citation,
                    "score": item.get("score", 0.0)
                })

        # 7. Validate answer support
        if not validate_answer_support(answer_text, sources):
            answer_text = (
                "The retrieved context is insufficient to support a confident answer. "
                "Please upload more relevant material or rephrase the question."
            )

        # 8. Final response
        return {
            "answer": answer_text,
            "sources": sources,
            "citations": citations,
            "retrieval_method": self.retrieval_method,
            "generation_mode": self.generation_mode,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "user_id": user_id,
        }

