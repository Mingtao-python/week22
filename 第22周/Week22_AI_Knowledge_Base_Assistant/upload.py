import hashlib
import os
from pathlib import Path
from typing import Any, Dict, Optional

from chunker import chunk_documents
from security.validation import parse_document, validate_file_metadata, parse_pdf_with_pages


class UploadManager:
    def __init__(self, rag_system: Any, upload_dir: str = "data/uploads"):
        self.rag = rag_system
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def _hash_content(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def upload_file(self, uploaded_file: Any, user_role: str = "student", metadata_base: Optional[Dict[str, Any]] = None):
        filename = (uploaded_file.filename or "").strip()
        if not filename:
            raise ValueError("File name is missing.")

        file_stream = uploaded_file.stream
        file_stream.seek(0)
        raw_bytes = file_stream.read()
        file_size = len(raw_bytes)

        mime_type = getattr(uploaded_file, "mimetype", None)
        valid, message = validate_file_metadata(filename, mime_type, file_size)
        if not valid:
            raise ValueError(message)

        ext = Path(filename).suffix.lower()
        
        if ext == ".pdf":
            return self._upload_pdf(raw_bytes, filename, user_role, metadata_base)
        
        # Standard handling for text files
        content = parse_document(raw_bytes, ext, filename)
        if not content or len(content.strip()) == 0:
            raise ValueError("The uploaded file is empty or unreadable.")

        content_hash = self._hash_content(content)
        existing = getattr(self.rag, "hashes", set())
        if content_hash in existing:
            raise ValueError("Duplicate file content detected; this document has already been uploaded.")

        document_id = f"doc-{len(self.rag.documents) + 1:04d}"
        safe_meta = {
            "document_id": document_id,
            "filename": filename,
            "user_role": user_role,
            "allowed_roles": ["student", "teacher", "admin"],
            "private": False,
            **(metadata_base or {}),
        }

        chunks = chunk_documents(
            content,
            size=350,
            overlap=50,
            document_id=document_id,
            filename=filename,
            page_map={"default": 1},
        )
        if not chunks:
            raise ValueError("Chunking produced no content.")

        texts = [item["text"] for item in chunks]
        docs_meta = []
        for chunk in chunks:
            item_meta = dict(safe_meta)
            item_meta.update({
                "chunk_id": chunk["chunk_id"],
                "page": chunk.get("page", 1),
                "filename": filename,
                "document_id": document_id,
            })
            docs_meta.append(item_meta)

        self.rag.add_documents(texts, docs_meta)
        self.rag.hashes.add(content_hash)

        return {
            "document_id": document_id,
            "filename": filename,
            "chunk_count": len(chunks),
            "hash": content_hash,
            "pages": 1,
        }

    def _upload_pdf(self, raw_bytes: bytes, filename: str, user_role: str, metadata_base: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle PDF file upload with proper page tracking.
        
        Returns:
            Dictionary with upload metadata including page count
        """
        # Parse PDF with page information
        page_map = parse_pdf_with_pages(raw_bytes, filename)
        
        if not page_map:
            raise ValueError("The PDF file is empty or contains no readable text.")
        
        # Create content hash from all pages
        all_content = "\n".join(page_map[p] for p in sorted(page_map.keys()))
        content_hash = self._hash_content(all_content)
        
        existing = getattr(self.rag, "hashes", set())
        if content_hash in existing:
            raise ValueError("Duplicate file content detected; this document has already been uploaded.")
        
        document_id = f"doc-{len(self.rag.documents) + 1:04d}"
        safe_meta = {
            "document_id": document_id,
            "filename": filename,
            "user_role": user_role,
            "allowed_roles": ["student", "teacher", "admin"],
            "private": False,
            **(metadata_base or {}),
        }
        
        # Process each page separately to maintain page information
        all_texts = []
        all_meta = []
        
        for page_num in sorted(page_map.keys()):
            page_content = page_map[page_num]
            
            # Chunk this page
            page_chunks = chunk_documents(
                page_content,
                size=350,
                overlap=50,
                document_id=document_id,
                filename=filename,
                page_map={"default": page_num},
            )
            
            # Add chunks with proper page metadata
            for chunk_idx, chunk in enumerate(page_chunks):
                item_meta = dict(safe_meta)
                item_meta.update({
                    "chunk_id": f"{document_id}-p{page_num}-{chunk_idx + 1:03d}",
                    "page": page_num,
                    "filename": filename,
                    "document_id": document_id,
                    "total_pages": len(page_map),
                })
                all_texts.append(chunk["text"])
                all_meta.append(item_meta)
        
        if not all_texts:
            raise ValueError("PDF processing produced no content.")
        
        # Add all chunks to the RAG system
        self.rag.add_documents(all_texts, all_meta)
        self.rag.hashes.add(content_hash)
        
        return {
            "document_id": document_id,
            "filename": filename,
            "chunk_count": len(all_texts),
            "hash": content_hash,
            "pages": len(page_map),
            "page_info": f"Successfully processed {len(page_map)} page(s)",
        }
