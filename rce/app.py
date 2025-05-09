from flask import Flask, request, render_template_string, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"php"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PHP Web Shell Upload</title>
    <style>
        body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
        input, button { font-family: monospace; background: #222; color: #0f0; border: 1px solid #0f0; padding: 5px; }
        pre { background: #000; padding: 10px; border: 1px solid #0f0; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h2>上傳 PHP Web Shell</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">上傳</button>
    </form>
    {% if link %}
    <h3>檔案已上傳：</h3>
    <a href="{{ link }}" target="_blank">{{ link }}</a>
    {% elif error %}
    <h3>錯誤：</h3>
    <pre>{{ error }}</pre>
    {% endif %}
</body>
</html>
"""

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    error = None
    link = None
    if request.method == "POST":
        if "file" not in request.files:
            error = "沒有檔案部份"
        else:
            file = request.files["file"]
            if file.filename == "":
                error = "未選擇檔案"
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                link = f"/uploads/{filename}"
            else:
                error = "只允許上傳 .php 檔案"
    return render_template_string(TEMPLATE, link=link, error=error)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/healthz")
def healthz():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
