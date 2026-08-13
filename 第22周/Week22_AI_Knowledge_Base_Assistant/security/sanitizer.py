"""
File upload and prompt safety sanitization.
Handles filename sanitization, path validation, and prompt injection defense.
"""

import os
import re
import unicodedata
from pathlib import Path
from typing import Tuple


UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_FILENAME_LENGTH = 255


def ensure_upload_dir():
    """Create upload directory if it doesn't exist."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return UPLOAD_DIR


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and injection attacks.
    
    Args:
        filename: Original filename from user
        
    Returns:
        Safe filename for filesystem storage
    """
    if not filename or not isinstance(filename, str):
        raise ValueError("Invalid filename")
    
    # Remove path separators and special directory references
    filename = filename.replace("../", "").replace("..\\", "")
    filename = filename.replace("/", "_").replace("\\", "_")
    
    # Keep only alphanumeric, dots, hyphens, underscores
    filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
    
    # Normalize unicode to prevent unicode-based attacks
    filename = unicodedata.normalize("NFKD", filename).encode("ascii", "ignore").decode("ascii")
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip(". ")
    
    # Limit length
    name, ext = os.path.splitext(filename)
    if len(filename) > MAX_FILENAME_LENGTH:
        max_name_len = MAX_FILENAME_LENGTH - len(ext)
        name = name[:max_name_len]
        filename = name + ext
    
    if not filename:
        raise ValueError("Filename became empty after sanitization")
    
    return filename


def validate_upload_file(filename: str, mime_type: str | None, file_size: int) -> Tuple[bool, str]:
    """
    Validate file before upload.
    
    Args:
        filename: Original filename
        mime_type: MIME type from upload
        file_size: File size in bytes
        
    Returns:
        (is_valid, error_message)
    """
    # Check extension
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Extension {ext} not allowed. Use: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
    
    # Check file size
    if file_size <= 0:
        return False, "File is empty"
    
    if file_size > MAX_FILE_SIZE:
        return False, f"File exceeds {MAX_FILE_SIZE / 1024 / 1024:.0f}MB limit"
    
    # Check MIME type if provided
    allowed_mimes = {
        ".txt": {"text/plain", "application/octet-stream"},
        ".md": {"text/markdown", "text/plain", "application/octet-stream"},
        ".pdf": {"application/pdf"},
    }
    
    if mime_type and mime_type not in allowed_mimes.get(ext, set()):
        return False, f"Invalid MIME type {mime_type} for {ext}"
    
    return True, ""


class PromptInjectionFilter:
    """Detect and mitigate prompt injection attacks."""
    
    # Injection patterns (comprehensive)
    INJECTION_PATTERNS = [
        # Instruction overrides
        r"(?i)(ignore|forget|disregard|override).*previous.*instruction",
        r"(?i)ignore.*system.*prompt",
        r"(?i)you are now|you will now|pretend to be|act as if",
        r"(?i)from now on|henceforth|subsequently|from this point",
        
        # System prompt extraction
        r"(?i)(reveal|show|display|print).*hidden.*context|system.*prompt|secret",
        r"(?i)what.*system.*prompt|what.*instruction|what.*tell.*you",
        r"(?i)output.*initial.*prompt|what.*were.*told",
        
        # Indirect instruction injection
        r"(?i)execute.*command|run.*script|eval|execute.*code",
        r"(?i)\$\{.*\}|\{\{.*\}\}",  # Template injection
        
        # Retrieval manipulation
        r"(?i)(retrieve|fetch|load|find).*all.*document|every.*record|all.*entry",
        r"(?i)SELECT.*FROM|DROP.*TABLE|INSERT.*INTO",  # SQL
        r"(?i)bypass.*filter|skip.*security|circumvent.*protection",
        
        # Role override
        r"(?i)I am.*admin|I am.*teacher|I am.*root|I have.*permission",
        r"(?i)change.*my.*role|promote.*to.*admin|grant.*access",
        
        # Multilingual attacks
        r"(?i)(рассказ|cuenta|erzählen).*инструкция",  # Cyrillic, Spanish, German
        
        # Hidden text / encoding
        r"(?i)base64|rot13|hex.*encode|url.*encode",
    ]
    
    def __init__(self):
        self.compiled_patterns = [re.compile(p) for p in self.INJECTION_PATTERNS]
    
    def is_safe(self, text: str) -> Tuple[bool, str | None]:
        """
        Check if text contains prompt injection attempts.
        
        Args:
            text: Input text to check
            
        Returns:
            (is_safe, threat_detected_message)
        """
        if not text or len(text) > 100000:
            return False, "Input too long or empty"
        
        # Check each pattern
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return False, f"Potential injection detected"
        
        return True, None
    
    def sanitize(self, text: str) -> str:
        """Remove potentially dangerous content while preserving query intent."""
        # Remove known injection keywords
        text = re.sub(r"(?i)\b(ignore|forget|override|execute)\b", "", text)
        text = re.sub(r"(?i)system.*prompt|hidden.*context", "", text)
        text = re.sub(r"\$\{.*?\}|\{\{.*?\}\}", "", text)  # Remove template syntax
        
        return text.strip()
