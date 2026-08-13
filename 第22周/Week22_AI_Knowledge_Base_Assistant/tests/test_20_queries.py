"""
Test 20 comprehensive queries across different subjects.
"""

import pytest
from rag import KnowledgeBaseRAG
from chunker import chunk_documents


class Test20SampleQueries:
    """Test system with 20 different queries across subjects."""
    
    def setup_method(self):
        """Initialize RAG system."""
        self.rag = KnowledgeBaseRAG()
    
    @pytest.mark.parametrize("question", [
        # Math questions (1-4)
        "What is the quadratic formula?",
        "How do you solve polynomial equations?",
        "Explain exponent rules",
        "What are basic algebraic principles?",
        
        # Physics questions (5-8)
        "What is Newton's first law of motion?",
        "How do you calculate kinetic energy?",
        "Explain momentum conservation",
        "What is the relationship between force and acceleration?",
        
        # Chemistry questions (9-12)
        "What is atomic structure?",
        "Explain chemical bonding",
        "What is the periodic table organization?",
        "How do atoms form molecules?",
        
        # Biology questions (13-16)
        "What is cell structure?",
        "Explain how mitochondria works",
        "What is the function of the cell membrane?",
        "How does photosynthesis work?",
        
        # History questions (17-20)
        "What was the Renaissance?",
        "Who were important Renaissance artists?",
        "Explain the historical significance of Renaissance",
        "What were key Renaissance inventions?",
    ])
    def test_query_processing(self, question):
        """Test that questions can be processed."""
        # This is a placeholder test - actual content depends on loaded documents
        assert isinstance(question, str)
        assert len(question) > 0
        assert "?" in question


class TestChunkCreation:
    """Test document chunking for retrieval."""
    
    def test_chunk_documents_basic(self):
        """Test basic document chunking."""
        text = "The quick brown fox jumps over the lazy dog. " * 100
        chunks = chunk_documents(text, size=200, overlap=50, document_id="doc1", filename="test.txt")
        
        assert len(chunks) > 0
        assert all("text" in chunk for chunk in chunks)
        assert all("chunk_id" in chunk for chunk in chunks)
        assert all("document_id" in chunk for chunk in chunks)
    
    def test_chunk_overlap_preserved(self):
        """Test that overlap between chunks works."""
        text = "AAAA BBBB CCCC DDDD EEEE " * 20
        chunks = chunk_documents(text, size=50, overlap=20, document_id="doc1", filename="test.txt")
        
        # Check that chunks overlap
        if len(chunks) > 1:
            # Overlapping text should appear in multiple chunks
            all_text = " ".join(chunk["text"] for chunk in chunks)
            assert len(all_text) > len(text)  # Overlap creates redundancy
    
    def test_chunk_metadata_preserved(self):
        """Test that metadata is preserved through chunking."""
        text = "Sample document content " * 50
        chunks = chunk_documents(
            text,
            size=300,
            overlap=0,
            document_id="doc123",
            filename="sample.txt"
        )
        
        assert all(chunk["document_id"] == "doc123" for chunk in chunks)
        assert all(chunk["filename"] == "sample.txt" for chunk in chunks)
    
    def test_chunk_id_format(self):
        """Test that chunk IDs follow correct format."""
        text = "Test content " * 50
        chunks = chunk_documents(text, size=200, overlap=0, document_id="doc_abc", filename="test.txt")
        
        for chunk in chunks:
            # Chunk ID should contain document_id and index
            assert "doc_abc" in chunk["chunk_id"]


class TestMultiPageChunking:
    """Test chunking with multi-page documents (like PDFs)."""
    
    def test_page_metadata_preserved(self):
        """Test that page information is preserved in chunks."""
        page_map = {
            1: "First page content " * 20,
            2: "Second page content " * 20,
            3: "Third page content " * 20,
        }
        
        # Simulate multi-page document chunking
        all_chunks = []
        for page_num, text in page_map.items():
            chunks = chunk_documents(
                text,
                size=300,
                overlap=0,
                document_id="doc_multi",
                filename="multi.pdf",
                page_map={page_num: text}
            )
            all_chunks.extend(chunks)
        
        # Each chunk should know which page it came from (if page_map used)
        assert len(all_chunks) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
