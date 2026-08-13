from flask import Flask, request, render_template_string, jsonify
from rag import KnowledgeBaseRAG
from upload import UploadManager

app = Flask(__name__)
rag_system = KnowledgeBaseRAG()
uploader = UploadManager(rag_system)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Knowledge Base Assistant</title>
</head>
<body>
    <h1>AI Knowledge Base Assistant (Mini RAG)</h1>
    <h2>Upload Document</h2>
    <form method="post" enctype="multipart/form-data" action="/upload">
        <input type="file" name="file">
        <input type="text" name="subject" placeholder="Subject">
        <input type="text" name="grade" placeholder="Grade">
        <button type="submit">Upload</button>
    </form>
    <h2>Ask Question</h2>
    <form method="post" action="/ask">
        <input type="text" name="question" style="width:400px">
        <button type="submit">Ask</button>
    </form>
    {% if answer %}
        <h3>Answer</h3>
        <p>{{ answer }}</p>
        <h3>Sources</h3>
        <ul>
        {% for s in sources %}
            <li>{{ s.text }} ({{ s.metadata }})</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML, answer=None, sources=[])

@app.route("/upload", methods=["POST"])
def upload():
    try:
        f = request.files.get("file")
        user_role = request.form.get("user_role", "student")
        subject = request.form.get("subject", "")
        grade = request.form.get("grade", "")
        
        if not f or f.filename == "":
            return jsonify({"error": "No file provided"}), 400

        metadata_base = {
            "subject": subject,
            "grade": grade,
            "user_role": user_role,
        }
        
        result = uploader.upload_file(f, user_role=user_role, metadata_base=metadata_base)
        return jsonify({
            "status": "success",
            "document_id": result["document_id"],
            "filename": result["filename"],
            "chunk_count": result["chunk_count"]
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route("/ask", methods=["POST"])
def ask():
    try:
        q = request.form.get("question", "")
        user_role = request.form.get("user_role", "student")
        top_k = int(request.form.get("top_k", "5"))
        
        if not q or not q.strip():
            return jsonify({"error": "Question cannot be empty"}), 400
        
        result = rag_system.answer(q, user_role=user_role, top_k=top_k)
        return render_template_string(HTML, answer=result["answer"], sources=result["sources"])
    except Exception as e:
        return jsonify({"error": f"Question processing failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
# :) dX