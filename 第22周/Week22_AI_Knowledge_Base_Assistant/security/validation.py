import os
from pathlib import Path

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
        try:
            return raw_bytes.decode("latin-1")
        except Exception:
            return raw_bytes.decode("utf-8", errors="replace")

    raise ValueError(f"Unsupported document extension: {ext}")
