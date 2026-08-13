from flask import Flask, request, render_template_string, jsonify
from rag import KnowledgeBaseRAG
from upload import UploadManager
from security.sanitizer import PromptInjectionFilter, ensure_upload_dir
from security.permissions_advanced import Permission
import logging

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB limit
rag_system = KnowledgeBaseRAG()
uploader = UploadManager(rag_system)
prompt_filter = PromptInjectionFilter()
ensure_upload_dir()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Knowledge Base Assistant - Secure Edition</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        input, select, textarea { width: 100%; padding: 8px; margin: 5px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .success { color: green; }
        .error { color: red; }
        .sources { background: #f5f5f5; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 AI Knowledge Base Assistant (Secure Edition)</h1>
        
        <div class="section">
            <h2>📤 Upload Document</h2>
            <form method="post" enctype="multipart/form-data" action="/upload">
                <input type="file" name="file" required>
                <input type="text" name="user_id" placeholder="Your User ID" required>
                <select name="user_role" required>
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                    <option value="admin">Admin</option>
                </select>
                <input type="text" name="subject" placeholder="Subject (e.g., Mathematics)">
                <input type="text" name="grade" placeholder="Grade (e.g., 10-12)">
                <input type="text" name="class_id" placeholder="Class ID (optional)">
                <label>
                    <input type="checkbox" name="private" value="true"> Private (only you can see)
                </label>
                <button type="submit">Upload Document</button>
            </form>
        </div>
        
        <div class="section">
            <h2>❓ Ask Question</h2>
            <form method="post" action="/ask">
                <textarea name="question" placeholder="Enter your question..." style="height: 100px;" required></textarea>
                <input type="text" name="user_id" placeholder="Your User ID" required>
                <select name="user_role" required>
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                    <option value="admin">Admin</option>
                </select>
                <input type="number" name="top_k" placeholder="Results to return" value="5" min="1" max="20">
                <button type="submit">Ask</button>
            </form>
        </div>
        
        {% if answer %}
            <div class="section">
                <h2>📝 Answer</h2>
                <p>{{ answer }}</p>
            </div>
        {% endif %}
        
        {% if sources %}
            <div class="section">
                <h2>📚 Sources</h2>
                <div class="sources">
                {% for s in sources %}
                    <div style="margin: 10px 0; padding: 10px; background: white; border-left: 3px solid #007bff;">
                        <p><strong>{{ s.metadata.filename }}</strong>
                        {% if s.metadata.page %}
                            (Page {{ s.metadata.page }}/{{ s.metadata.total_pages or 1 }})
                        {% endif %}</p>
                        <p>{{ s.text[:200] }}...</p>
                        <p style="font-size: 0.9em; color: #666;">
                            Score: {{ "%.3f" % s.score }}
                        </p>
                    </div>
                {% endfor %}
                </div>
            </div>
        {% endif %}
        
        <div class="section" style="background: #e8f4f8; border-left: 4px solid #17a2b8;">
            <h3>🔒 Security Features</h3>
            <ul>
                <li>✓ Filename sanitization & path traversal protection</li>
                <li>✓ Prompt injection detection & mitigation</li>
                <li>✓ Granular permission control (role-based & class-based)</li>
                <li>✓ Accurate cosine similarity search with normalization</li>
                <li>✓ Multi-page PDF support with page tracking</li>
                <li>✓ 10MB file size limit & MIME type validation</li>
                <li>✓ Secure logging & error handling</li>
            </ul>
        </div>
    </div>
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
        user_id = request.form.get("user_id", "anonymous")
        user_role = request.form.get("user_role", "student")
        subject = request.form.get("subject", "")
        grade = request.form.get("grade", "")
        class_id = request.form.get("class_id", "")
        private = request.form.get("private", "false").lower() == "true"
        
        if not f or f.filename == "":
            return jsonify({"error": "No file provided"}), 400
        
        # Security: validate file before processing
        from security.sanitizer import validate_upload_file, sanitize_filename
        is_valid, error_msg = validate_upload_file(f.filename, f.content_type, len(f.read()))
        f.seek(0)  # Reset file pointer
        
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # Sanitize filename
        safe_filename = sanitize_filename(f.filename)
        
        # Prepare metadata with permissions
        metadata_base = {
            "subject": subject,
            "grade": grade,
            "user_role": user_role,
        }
        
        # Add permission metadata
        Permission.add_permission(
            metadata_base,
            owner_id=user_id,
            allowed_roles=["student", "teacher"] if user_role == "teacher" else ["student"],
            class_id=class_id if class_id else None,
            private=private
        )
        
        result = uploader.upload_file(f, user_role=user_role, metadata_base=metadata_base)
        logger.info(f"File uploaded: {safe_filename} by {user_id}")
        
        return jsonify({
            "status": "success",
            "document_id": result["document_id"],
            "filename": result["filename"],
            "chunk_count": result["chunk_count"],
            "pages": result.get("pages", 1)
        })
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route("/ask", methods=["POST"])
def ask():
    try:
        q = request.form.get("question", "")
        user_id = request.form.get("user_id", "anonymous")
        user_role = request.form.get("user_role", "student")
        top_k = int(request.form.get("top_k", "5"))
        
        if not q or not q.strip():
            return jsonify({"error": "Question cannot be empty"}), 400
        
        # Security: check for prompt injection
        is_safe, threat_msg = prompt_filter.is_safe(q)
        if not is_safe:
            logger.warning(f"Potential injection from {user_id}: {threat_msg}")
            return jsonify({"error": "Question contains potentially malicious content"}), 400
        
        # Process question through RAG with permission checking
        result = rag_system.answer(
            q, 
            user_id=user_id,
            user_role=user_role, 
            top_k=top_k,
            permission_checker=lambda meta: Permission.can_access(user_id, user_role, meta)
        )
        
        logger.info(f"Question answered for {user_id}: {q[:50]}...")
        return render_template_string(HTML, answer=result["answer"], sources=result["sources"])
    except Exception as e:
        logger.error(f"Question processing error: {str(e)}")
        return jsonify({"error": f"Question processing failed: {str(e)}"}), 500

if __name__ == "__main__":
    # Production: disable debug mode
    # Development: set DEBUG=true environment variable
    import os
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, host="127.0.0.1", port=5000)