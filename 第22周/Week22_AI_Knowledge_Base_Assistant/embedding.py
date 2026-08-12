from typing import Iterable, List, Union

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.model_version = getattr(self.model, "_model_card_vars", {}).get("version", "unknown") or "unknown"
        self.vector_dim = int(self.model.get_sentence_embedding_dimension())
        self.retrieval_method = "SentenceTransformer Embedding"

    def encode(self, texts: Union[str, Iterable[str]]) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(list(texts), convert_to_numpy=True, normalize_embeddings=True)
        return np.asarray(embeddings, dtype=np.float32)
