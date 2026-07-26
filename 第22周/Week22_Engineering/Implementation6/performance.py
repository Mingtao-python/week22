import numpy as np
from sentence_transformers import SentenceTransformer

def chunk_text(text, size):
    return [text[i:i+size] for i in range(0, len(text), size)]

def top1(vecs, q_vec):
    scores = np.dot(vecs, q_vec)
    return int(np.argmax(scores))

def test_chunk_size(doc, query, sizes):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    q_vec = model.encode([query])[0]
    results = {}
    for s in sizes:
        chunks = chunk_text(doc, s)
        vecs = model.encode(chunks)
        results[s] = top1(vecs, q_vec)
    return results

if __name__ == "__main__":
    long_doc = (
        "Python is a programming language widely used for AI, data science, automation, "
        "web development, and education. It provides simple syntax and powerful libraries "
        "such as NumPy, Pandas, TensorFlow, and PyTorch. Python is also used in machine "
        "learning, natural language processing, and backend systems. Many developers prefer "
        "Python because it is easy to learn and has a large community. Python supports "
        "object-oriented programming, functional programming, and scripting. It is one of "
        "the most popular languages in the world."
    )

    query = "python programming language"
    sizes = [100, 300, 500]
    print(test_chunk_size(long_doc, query, sizes))
