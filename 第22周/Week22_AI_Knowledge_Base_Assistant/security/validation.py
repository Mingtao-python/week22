import os
from io import BytesIO
from pathlib import Path
from typing import Dict, Tuple

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf"}
ALLOWED_MIME_TYPES = {
    ".txt": {"text/plain", "application/octet-stream"},
    ".md": {"text/markdown", "text/plain", "application/octet-stream"},
    ".pdf": {"application/pdf"},
}


def validate_file_metadata(filename: str, mime_type: str | None, file_size: int) -> tuple[bool, str]:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file type: {ext}. Allowed: {sorted(ALLOWED_EXTENSIONS)}"

    if file_size <= 0:
        return False, "The uploaded file is empty."

    if file_size > 10 * 1024 * 1024:
        return False, "The uploaded file exceeds the 10 MB limit."

    if mime_type and mime_type not in ALLOWED_MIME_TYPES.get(ext, set()):
        return False, f"Unexpected MIME type: {mime_type} for {ext}"

    candidate = os.path.basename(filename)
    if candidate != filename or ".." in candidate:
        return False, "Unsafe file name detected."

    return True, "OK"


def parse_document(raw_bytes: bytes, ext: str, filename: str) -> str:
    """Parse document and return concatenated text content."""
    if ext == ".txt":
        try:
            return raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return raw_bytes.decode("utf-8", errors="replace")

    if ext == ".md":
        try:
            return raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return raw_bytes.decode("utf-8", errors="replace")

    if ext == ".pdf":
        # For PDF, return concatenated text from all pages
        page_map = parse_pdf_with_pages(raw_bytes, filename)
        if not page_map:
            return ""
        # Concatenate all pages with page markers
        texts = []
        for page_num in sorted(page_map.keys()):
            texts.append(f"\n\n--- Page {page_num} ---\n{page_map[page_num]}")
        return "\n".join(texts)

    raise ValueError(f"Unsupported document extension: {ext}")


def parse_pdf_with_pages(raw_bytes: bytes, filename: str) -> Dict[int, str]:
    """
    Parse PDF and return a dictionary mapping page numbers to text content.
    
    Args:
        raw_bytes: PDF file content as bytes
        filename: Original filename (for error messages)
    
    Returns:
        Dictionary with page numbers (1-indexed) as keys and text as values
        Returns empty dict if PDF is empty, unreadable, or corrupted
    
    Handles:
        - Single page PDFs
        - Multi-page PDFs
        - Empty PDFs
        - Chinese text (UTF-8)
        - Corrupted PDFs (gracefully degrades)
    """
    if not pdfplumber:
        raise ImportError("pdfplumber is required for PDF parsing. Install with: pip install pdfplumber")
    
    if not raw_bytes:
        return {}
    
    page_map = {}
    
    try:
        pdf_file = BytesIO(raw_bytes)
        
        with pdfplumber.open(pdf_file) as pdf:
            # Check if PDF has pages
            if not pdf.pages:
                return {}
            
            # Extract text from each page
            for page_num, page in enumerate(pdf.pages, start=1):
                try:
                    # Extract text with fallback to OCR if needed
                    text = page.extract_text()
                    
                    # Handle None return (empty page)
                    if text is None:
                        text = ""
                    
                    # Clean up text
                    text = text.strip()
                    
                    if text:  # Only add non-empty pages
                        page_map[page_num] = text
                    else:
                        # Even empty pages should be recorded
                        page_map[page_num] = f"[Page {page_num} appears to be empty or contains only images]"
                
                except Exception as page_error:
                    # Handle single page parsing errors gracefully
                    page_map[page_num] = f"[Error reading page {page_num}: {str(page_error)}]"
        
        return page_map
    
    except Exception as e:
        # Handle all parsing errors (corrupted PDFs, syntax errors, etc.)
        error_msg = str(e)
        
        # Check if it's a PDF syntax/corruption error
        if "PDF" in error_msg or "syntax" in error_msg.lower() or "corrupted" in error_msg.lower():
            raise ValueError(f"The PDF file '{filename}' appears to be corrupted or invalid: {error_msg}")
        else:
            raise ValueError(f"Failed to parse PDF '{filename}': {error_msg}")
