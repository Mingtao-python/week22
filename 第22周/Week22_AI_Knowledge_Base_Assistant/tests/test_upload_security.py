"""
Test file upload and filename sanitization.
"""

import pytest
from pathlib import Path
from security.sanitizer import sanitize_filename, validate_upload_file, ensure_upload_dir


class TestFilenameSanitization:
    """Test filename sanitization against attacks."""
    
    def test_path_traversal_removed(self):
        """Test that path traversal sequences are removed."""
        assert ".." not in sanitize_filename("../../../etc/passwd")
        assert "/" not in sanitize_filename("../../config.txt")
    
    def test_special_chars_removed(self):
        """Test that special characters are converted."""
        result = sanitize_filename("file<>:?*|.txt")
        assert all(c not in result for c in "<>:?*|")
    
    def test_unicode_normalization(self):
        """Test that unicode is normalized to ASCII safe version."""
        result = sanitize_filename("файл.txt")  # Russian chars
        assert result.isascii()
    
    def test_leading_trailing_stripped(self):
        """Test that leading/trailing dots are removed."""
        assert not sanitize_filename("...file...").startswith(".")
        assert not sanitize_filename("...file...").endswith(".")
    
    def test_long_filename_truncated(self):
        """Test that very long filenames are truncated."""
        long_name = "a" * 300 + ".txt"
        result = sanitize_filename(long_name)
        assert len(result) <= 260  # 255 + some buffer


class TestUploadValidation:
    """Test file validation before upload."""
    
    def test_invalid_extension_rejected(self):
        """Test that disallowed extensions are rejected."""
        is_valid, msg = validate_upload_file("file.exe", "application/exe", 1024)
        assert not is_valid
        assert "not allowed" in msg.lower()
    
    def test_empty_file_rejected(self):
        """Test that empty files are rejected."""
        is_valid, msg = validate_upload_file("file.txt", "text/plain", 0)
        assert not is_valid
        assert "empty" in msg.lower()
    
    def test_oversized_file_rejected(self):
        """Test that files exceeding 10MB are rejected."""
        is_valid, msg = validate_upload_file("file.txt", "text/plain", 11 * 1024 * 1024)
        assert not is_valid
        assert "exceed" in msg.lower() or "limit" in msg.lower()
    
    def test_invalid_mime_rejected(self):
        """Test that mismatched MIME types are rejected."""
        is_valid, msg = validate_upload_file("file.pdf", "text/plain", 1024)
        assert not is_valid
        assert "mime" in msg.lower()
    
    def test_valid_txt_accepted(self):
        """Test that valid text files are accepted."""
        is_valid, msg = validate_upload_file("file.txt", "text/plain", 1024)
        assert is_valid
        assert msg == ""
    
    def test_valid_pdf_accepted(self):
        """Test that valid PDF files are accepted."""
        is_valid, msg = validate_upload_file("document.pdf", "application/pdf", 5000000)
        assert is_valid
        assert msg == ""


class TestUploadDirectory:
    """Test upload directory management."""
    
    def test_upload_dir_created(self):
        """Test that upload directory is created."""
        upload_dir = ensure_upload_dir()
        assert upload_dir.exists()
        assert upload_dir.is_dir()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
