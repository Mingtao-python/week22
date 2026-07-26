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
    docs = ["learn python basics", 
            "python tutorial for beginners", 
            "best python online course", 
            "advanced python programming guide", 
            "java basics introduction", 
            "how to cook simple meals", 
            "how to learn english effectively", 
            "machine learning fundamentals", 
            "deep learning introduction", 
            "neural network explanation", 
            "what is semantic search", 
            "vector database overview", 
            "how to improve study habits", 
            "tips for learning languages", 
            "bank financial services", 
            "river bank natural landscape", 
            "apple fruit nutrition facts", 
            "apple company history", 
            "python vs java comparison", 
            "how to bake bread at home", 
            "travel tips for europe", 
            "healthy eating guidelines", 
            "beginner guide to meditation", 
            "how to fix common computer issues", 
            "cloud computing basics", 
            "introduction to data science", 
            "how to start running", 
            "best practices for cybersecurity", 
            "guide to personal finance", 
            "how to write better essays", 
            "history of artificial intelligence", 
            "what is reinforcement learning", 
            "how to clean your room efficiently", 
            "tips for time management", 
            "how to choose a laptop", 
            "beginner guide to cooking", 
            "how to learn math faster", 
            "importance of sleep for health", 
            "how to practice speaking english", 
            "basic guitar chords tutorial", 
            "introduction to blockchain", 
            "cryptocurrency safety tips", 
            "how to organize your workspace", 
            "what is natural language processing", 
            "how to take better photos", 
            "beginner guide to gardening", 
            "how to reduce stress", 
            "simple home workout routines"]
# note: sentences created by AI copilot
    engine = SemanticRetrieval()
    engine.add(docs)
    for n in ['how to learn python quickly', 
'python vs java which is better', 
'best way to improve english speaking', 
'what is machine learning', 
'explain neural networks simply', 
'how to cook healthy meals', 
'tips for reducing stress', 
'bank near the river', 
'bank financial loan information', 
'apple company products', 
'apple fruit health benefits', 
'how to start learning data science', 
'what is semantic search', 
'how to take better photos', 
'beginner guide to meditation', 
'how to choose a laptop for school', 
'how to learn math faster', 
'what is blockchain technology', 
'how to organize your workspace', 
'simple home workout routine'
]:
        print(n, engine.search(n, top_k=3))
