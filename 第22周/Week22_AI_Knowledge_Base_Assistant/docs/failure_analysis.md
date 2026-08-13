# Failure Analysis

## Common failure modes

1. Unsupported file types
2. Empty or malformed files
3. Duplicate document uploads
4. Unsafe file names
5. Insufficient evidence for question answering
6. Permission violations

## Handling strategy

- Reject unsupported inputs before index insertion
- Surface explicit validation error messages in the UI
- Filter documents by role before retrieval
- Return a safe "insufficient context" message when evidence is weak

## Metrics tracking

Failure categories can be counted and traced to specific test cases, rather than being hard-coded into the product output.
