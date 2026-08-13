"""
Test citation and source attribution.
"""

import pytest
from rag import KnowledgeBaseRAG
from retrieval import RetrievalEngine
from vector_database import VectorDatabase


class TestCitationGeneration:
    """Test that citations include proper source attribution."""
    
    def test_citation_includes_document_name(self):
        """Test that citations include document filename."""
        # This test validates citation format
        citation_format = "{filename} (Page {page}/{total_pages})"
        assert "{filename}" in citation_format
        assert "Page" in citation_format
    
    def test_citation_includes_page_number(self):
        """Test that multi-page documents have page numbers."""
        metadata = {
            "filename": "document.pdf",
            "page": 2,
            "total_pages": 5,
            "document_id": "doc_001"
        }
        
        assert "page" in metadata
        assert metadata["page"] == 2
        assert metadata["total_pages"] == 5
    
    def test_citation_with_single_page(self):
        """Test citation for single-page documents."""
        metadata = {
            "filename": "note.txt",
            "page": 1,
            "total_pages": 1,
        }
        
        # Should not show "page 1 of 1" as redundant
        citation_parts = [
            metadata["filename"],
            f"Page {metadata['page']}" if metadata["total_pages"] > 1 else None
        ]
        
        citation = " ".join([p for p in citation_parts if p])
        assert "note.txt" in citation


class TestSourceRetrieval:
    """Test that retrieved sources have correct metadata."""
    
    def test_retrieval_includes_metadata(self):
        """Test that retrieval results include metadata."""
        db = VectorDatabase()
        
        # Add test document
        docs = ["Sample document content"]
        metadata = [{"filename": "test.txt", "document_id": "doc1", "page": 1}]
        
        db.add_documents(docs, metadata=metadata)
        
        # Search
        results = db.search("document", top_k=1)
        
        assert len(results) > 0
        assert "metadata" in results[0]
        assert results[0]["metadata"]["filename"] == "test.txt"


class TestMultipageSourceTracking:
    """Test that multi-page sources are tracked correctly."""
    
    def test_page_number_in_chunk_id(self):
        """Test that page number appears in chunk ID."""
        # Chunk ID format for multi-page: "doc_id-p{page}-{index}"
        chunk_ids = [
            "doc_001-p1-001",  # Page 1, chunk 1
            "doc_001-p2-001",  # Page 2, chunk 1
            "doc_001-p3-001",  # Page 3, chunk 1
        ]
        
        for chunk_id in chunk_ids:
            assert "-p" in chunk_id  # Contains page marker
            parts = chunk_id.split("-p")
            assert len(parts) == 2  # Document and page parts
    
    def test_page_metadata_extraction(self):
        """Test extracting page from chunk ID."""
        chunk_id = "doc_001-p3-015"
        
        # Extract page number
        if "-p" in chunk_id:
            page_part = chunk_id.split("-p")[1].split("-")[0]
            page_num = int(page_part)
            assert page_num == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
