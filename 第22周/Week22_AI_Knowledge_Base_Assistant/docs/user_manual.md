# User Manual

## Upload

1. Open the web app at http://localhost:5000.
2. Select a PDF, TXT, or Markdown file.
3. Choose a role: student, teacher, or admin.
4. Submit the file.
5. The system validates file type, file size, duplicate content, and safe naming.

## Ask questions

1. Enter a question in the Q&A form.
2. Select a role.
3. Submit the form.
4. The system retrieves relevant chunks using sentence-transformer embeddings and filters by role.
5. The returned answer includes citations.

## Notes

- Student access can be limited by document permissions.
- Teacher and admin roles have broader document access.
- The system reports retrieval method explicitly as `SentenceTransformer Embedding`.
