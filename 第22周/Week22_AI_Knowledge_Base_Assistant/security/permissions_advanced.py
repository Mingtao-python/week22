"""
Granular permission control system for document access.
Supports role-based and class-based access control.
"""

from typing import Dict, List, Any
from enum import Enum


class UserRole(Enum):
    """Supported user roles."""
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    OWNER = "owner"


class Permission:
    """Permission checking for document access."""
    
    @staticmethod
    def can_access(user_id: str, user_role: str, document_metadata: Dict[str, Any]) -> bool:
        """
        Check if user can access document.
        
        Args:
            user_id: User identifier
            user_role: User role (student, teacher, admin, owner)
            document_metadata: Document metadata dict with:
                - owner: document owner user_id
                - allowed_roles: list of allowed roles
                - class_id: class identifier (optional)
                - private: boolean privacy flag
                
        Returns:
            True if user can access, False otherwise
        """
        if not document_metadata:
            return False
        
        # Admin can access everything
        if user_role == "admin":
            return True
        
        # Owner can always access their own documents
        if user_role == "owner" or user_id == document_metadata.get("owner"):
            return True
        
        # Check privacy flag
        if document_metadata.get("private", False):
            # Only owner and admin can access private documents
            return user_id == document_metadata.get("owner") or user_role == "admin"
        
        # Check allowed roles
        allowed_roles = document_metadata.get("allowed_roles", [])
        if allowed_roles and user_role not in allowed_roles:
            return False
        
        # Check class membership if specified
        if "class_id" in document_metadata:
            user_classes = getattr(Permission, "_user_classes", {}).get(user_id, [])
            if document_metadata["class_id"] not in user_classes:
                # Non-students in the same class can still access
                if user_role != "teacher":
                    return False
        
        return True
    
    @staticmethod
    def can_modify(user_id: str, user_role: str, document_metadata: Dict[str, Any]) -> bool:
        """
        Check if user can modify/delete document.
        Only owner and admin can modify.
        """
        if user_role == "admin":
            return True
        
        return user_id == document_metadata.get("owner")
    
    @staticmethod
    def add_permission(metadata: Dict[str, Any], 
                      owner_id: str,
                      allowed_roles: List[str] = None,
                      class_id: str = None,
                      private: bool = False) -> Dict[str, Any]:
        """
        Add permission metadata to document.
        
        Args:
            metadata: Existing metadata dict
            owner_id: User ID of document owner
            allowed_roles: List of allowed roles (student, teacher, admin)
            class_id: Class ID for class-level sharing
            private: Whether document is private
            
        Returns:
            Enhanced metadata dict
        """
        metadata["owner"] = owner_id
        metadata["allowed_roles"] = allowed_roles or ["student", "teacher"]
        if class_id:
            metadata["class_id"] = class_id
        metadata["private"] = private
        
        return metadata
