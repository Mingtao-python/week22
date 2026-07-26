import os
import markdown
from validation import validate_document
from rag import MiniRAGSystem

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_md(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(path):
    # 简化版：真实项目用 PyPDF2 或 pdfplumber
    return "PDF content placeholder"

def chunk_text(text, size=500):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks

class UploadManager:
    def __init__(self, rag_system: MiniRAGSystem):
        self.rag = rag_system

    def upload_file(self, filepath, metadata_base=None):
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".txt":
            content = read_txt(filepath)
        elif ext == ".md":
            content = read_md(filepath)
        elif ext == ".pdf":
            content = read_pdf(filepath)
        else:
            return False

        if not validate_document(content):
            return False

        chunks = chunk_text(content, size=500)
        metas = []
        for i, c in enumerate(chunks):
            m = metadata_base.copy() if metadata_base else {}
            m["chunk_id"] = i
            metas.append(m)

        self.rag.add_docs(chunks, metas)
        return True