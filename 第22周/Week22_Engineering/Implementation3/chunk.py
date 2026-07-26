def chunk_text(text, size):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks

if __name__ == "__main__":
    text = "A" * 2000
    for size in [100, 300, 500]:
        chunks = chunk_text(text, size)
        print(size, len(chunks))
