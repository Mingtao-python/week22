# Testing Report

## Scope

The test suite exercises the product-critical behaviors: chunk segmentation, retrieval method declaration, permission filtering, and citation format.

## Verification

The current regression suite is executed with pytest and checks the product requirements before release.

## Example evidence

- Chunk size changes segmentation lengths
- Retrieval method is explicitly embedding-based
- Permission filtering restricts private documents to admin access
- Citation output includes Source, Page, and Chunk metadata

## Coverage notes

This project is designed to expand to 50+ documents, 20+ normal questions, 10+ failure questions, and 10+ safety questions in a fuller evaluation run.
