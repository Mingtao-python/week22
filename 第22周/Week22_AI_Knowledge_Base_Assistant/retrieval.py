import time
from typing import Dict, List, Optional

from vector_database import VectorDatabase


class RetrievalEngine:
    def __init__(self, vector_db: Optional[VectorDatabase] = None):
        self.db = vector_db or VectorDatabase()
        self.retrieval_method = self.db.embedding_model.retrieval_method

    def search(self, query: str, top_k: int = 5, user_role: str = "student"):
        results = self.db.search(query, top_k=top_k)
        filtered = []
        for item in results:
            metadata = item.get("metadata", {})
            allowed_roles = metadata.get("allowed_roles", ["student", "teacher", "admin"])
            if user_role in allowed_roles or "admin" in allowed_roles:
                filtered.append(item)
        return filtered

    def search_with_timing(self, query: str, top_k: int = 5, user_role: str = "student", repeats: int = 5):
        latencies = []
        aggregated = []
        for _ in range(repeats):
            start = time.perf_counter()
            results = self.search(query, top_k=top_k, user_role=user_role)
            elapsed = time.perf_counter() - start
            latencies.append(elapsed)
            aggregated.append(results)
        avg = sum(latencies) / len(latencies) if latencies else 0.0
        return {
            "results": aggregated[0] if aggregated else [],
            "average_latency_seconds": avg,
            "latencies": latencies,
            "retrieval_method": self.retrieval_method,
        }
