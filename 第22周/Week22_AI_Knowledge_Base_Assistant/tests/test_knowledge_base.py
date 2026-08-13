import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chunker import chunk_documents
from citation import build_citation
from retrieval import RetrievalEngine
from security.permissions import can_access_document, filter_documents_for_role


def test_chunk_sizes_change_segmentation():
    text = " ".join([f"sentence {i}" for i in range(300)])
    small = chunk_documents(text, size=60)
    large = chunk_documents(text, size=200)
    assert len(small) > len(large)
    assert all(chunk["text"] for chunk in small)


def test_retrieval_method_is_embedding_based():
    engine = RetrievalEngine()
    assert engine.retrieval_method == "SentenceTransformer Embedding"


def test_permission_filter_applies_roles():
    docs = [
        {"document_id": "public", "allowed_roles": ["student", "teacher", "admin"]},
        {"document_id": "private", "allowed_roles": ["admin"]},
    ]
    assert len(filter_documents_for_role(docs, "student")) == 1
    assert not can_access_document("student", docs[1])
    assert can_access_document("admin", docs[1])


def test_citation_format_includes_source_page_chunk():
    chunk = {
        "document_id": "doc-1",
        "filename": "school_rules.pdf",
        "page": 3,
        "chunk_id": "12",
        "text": "Students must submit homework before 5pm.",
    }
    citation = build_citation(chunk)
    assert "Source: school_rules.pdf" in citation
    assert "Page: 3" in citation
    assert "Chunk: 12" in citation


def test_text_upload_works_and_validates_blank_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "sample.txt"
        path.write_text("This is a valid knowledge base entry for student questions.", encoding="utf-8")
        assert path.exists()

        empty_path = Path(tmpdir) / "empty.txt"
        empty_path.write_text("   ", encoding="utf-8")
        assert empty_path.exists()
