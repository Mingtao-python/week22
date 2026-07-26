from flask import Flask, request, render_template_string
from src.rag import MiniRAGSystem
from src.upload import UploadManager

app = Flask(__name__)
rag_system = MiniRAGSystem()
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
    f = request.files.get("file")
    subject = request.form.get("subject", "")
    grade = request.form.get("grade", "")
    if not f:
        return "No file", 400

    path = "uploaded_" + f.filename
    f.save(path)
    metadata = {"subject": subject, "grade": grade, "private": False}
    ok = uploader.upload_file(path, metadata_base=metadata)
    return "Uploaded" if ok else "Upload failed"

@app.route("/ask", methods=["POST"])
def ask():
    q = request.form.get("question", "")
    result = rag_system.answer(q, user_role="student", top_k=3)
    return render_template_string(HTML, answer=result["answer"], sources=result["sources"])

if __name__ == "__main__":
    app.run(debug=True)
# :) dX