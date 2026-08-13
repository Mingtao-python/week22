"""
Test granular permission control system.
"""

import pytest
from security.permissions_advanced import Permission


class TestPermissionControl:
    """Test permission checking for document access."""
    
    def test_admin_can_access_anything(self):
        """Test that admin can access any document."""
        metadata = {
            "owner": "user1",
            "private": True,
            "allowed_roles": []
        }
        assert Permission.can_access("admin_user", "admin", metadata)
    
    def test_owner_can_access_own_document(self):
        """Test that owner can access their own document."""
        metadata = {
            "owner": "user1",
            "private": True,
            "allowed_roles": []
        }
        assert Permission.can_access("user1", "owner", metadata)
    
    def test_student_cannot_access_private(self):
        """Test that student cannot access private documents."""
        metadata = {
            "owner": "user1",
            "private": True,
            "allowed_roles": ["teacher"]
        }
        assert not Permission.can_access("user2", "student", metadata)
    
    def test_student_can_access_public(self):
        """Test that student can access public documents."""
        metadata = {
            "owner": "user1",
            "private": False,
            "allowed_roles": ["student", "teacher"]
        }
        assert Permission.can_access("user2", "student", metadata)
    
    def test_teacher_respects_allowed_roles(self):
        """Test that teacher role is checked."""
        metadata = {
            "owner": "user1",
            "private": False,
            "allowed_roles": ["teacher"]
        }
        assert Permission.can_access("user2", "teacher", metadata)
    
    def test_student_excluded_from_teacher_only(self):
        """Test that student is excluded from teacher-only documents."""
        metadata = {
            "owner": "user1",
            "private": False,
            "allowed_roles": ["teacher"]
        }
        assert not Permission.can_access("user2", "student", metadata)
    
    def test_class_based_access(self):
        """Test class-based document access."""
        metadata = {
            "owner": "user1",
            "private": False,
            "class_id": "class_101",
            "allowed_roles": ["student", "teacher"]
        }
        # Note: Without user_classes registry, this will depend on implementation
        # For now, teacher should always access
        assert Permission.can_access("teacher_user", "teacher", metadata)
    
    def test_can_modify_only_owner_and_admin(self):
        """Test that only owner and admin can modify."""
        metadata = {"owner": "user1"}
        
        # Owner can modify
        assert Permission.can_modify("user1", "owner", metadata)
        
        # Admin can modify
        assert Permission.can_modify("admin_user", "admin", metadata)
        
        # Others cannot
        assert not Permission.can_modify("user2", "student", metadata)
        assert not Permission.can_modify("user2", "teacher", metadata)


class TestPermissionMetadata:
    """Test permission metadata creation."""
    
    def test_add_permission_sets_owner(self):
        """Test that owner is set correctly."""
        metadata = {}
        result = Permission.add_permission(metadata, owner_id="user1")
        assert result["owner"] == "user1"
    
    def test_add_permission_sets_roles(self):
        """Test that allowed roles are set."""
        metadata = {}
        result = Permission.add_permission(
            metadata,
            owner_id="user1",
            allowed_roles=["student", "teacher"]
        )
        assert "student" in result["allowed_roles"]
        assert "teacher" in result["allowed_roles"]
    
    def test_add_permission_sets_class_id(self):
        """Test that class_id is set."""
        metadata = {}
        result = Permission.add_permission(
            metadata,
            owner_id="user1",
            class_id="class_101"
        )
        assert result["class_id"] == "class_101"
    
    def test_add_permission_sets_private_flag(self):
        """Test that private flag is set."""
        metadata = {}
        result = Permission.add_permission(
            metadata,
            owner_id="user1",
            private=True
        )
        assert result["private"] is True
    
    def test_default_teacher_permissions(self):
        """Test default permissions for teacher-uploaded document."""
        metadata = {}
        result = Permission.add_permission(
            metadata,
            owner_id="teacher1",
            allowed_roles=["student"]
        )
        assert result["allowed_roles"] == ["student"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
