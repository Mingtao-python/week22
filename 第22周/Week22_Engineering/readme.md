# Week22 Engineering

This folder contains experimental implementations and analysis for Week 22 of the AI engineering assignment. Each subfolder demonstrates a different retrieval, vector database, or RAG-related concept.

## Project Structure
Copied from PowerShell
```
D:.
│  readme.md
│  testing_report.md
│  requirement.txt
|
├─Implementation1
│  │   example.png
│  └─  Vector_Database.py
│
├─Implementation2
│  │  example.png
│  └─ faiss_search.py
│
├─Implementation3
│  │  chunk.py
│  └─ example.png
|
├─Implementation4
│  │  example.png
│  └─ retrieval.py
│
├─Implementation5
│  │  example.png
│  └─ rag.py
│
├─Implementation6
│  │  example.png
│  └─ performance.py
│
└─Implementation7
        example.png
        failure_analysis.py
```

## Dependencies

- Python 3.10
- numpy
- sentence-transformers
- faiss (for Implementation2)
- Windows system

## Usage

1. Install dependencies in a Python environment.
  ```powershell
    pip.exe install -r requirement.txt
  ```
2. Run individual implementation scripts to explore each concept.
   ```powershell
   python .\Implementation1\Vector_Database.py
   python .\Implementation2\faiss_search.py
   python .\Implementation3\chunk.py
   python .\Implementation4\retrieval.py
   python .\Implementation5\rag.py
   python .\Implementation6\performance.py
   python .\Implementation7\failure_analysis.py
   ```

## Notes

- `Implementation1` and `Implementation5` focus on the end-to-end retrieval and RAG workflow.
- `Implementation2` shows how to leverage FAISS for efficient vector search.
- `Implementation3` and `Implementation6` are useful for understanding how chunk size impacts retrieval and performance.
- `Implementation7` highlights common retrieval failure scenarios.

## Related Project

A companion AI knowledge base assistant project exists in `Week22_AI_Knowledge_Base_Assistant/`, which includes a small Flask app, upload manager, and mini RAG system.  
Copied from PowerShell  
```
D:.  
│  app.py  
│  
└─src  
        rag.py  
        upload.py  
        validation.py  
        vector_database.py
```