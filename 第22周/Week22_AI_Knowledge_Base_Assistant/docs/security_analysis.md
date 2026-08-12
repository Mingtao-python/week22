# Security Analysis

## Document validation

- Extension validation for `.txt`, `.md`, and `.pdf`
- MIME validation
- File size validation
- Empty file detection
- Duplicate file detection
- Safe filename restrictions

## Role-based access

The system supports three roles:

- student
- teacher
- admin

Role filtering is applied before retrieval so the model does not search privileged documents and then hide results later.

## Risk handling

- Unsafe filenames are rejected
- Duplicate content is blocked
- Documents are assigned role permissions before indexing
- Retrieval uses the role-aware metadata to enforce access control
