# simplecloud.py  – Read & write files on wavy's Desktop
from flask import Flask, request, send_from_directory, jsonify, abort
from werkzeug.utils import secure_filename
import os

# === configuration =======================================================
DESKTOP = "/home/wavy/Desktop"      # exact path for user 'wavy'
print("Serving files from:", DESKTOP)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024   # 100 MB upload cap

# === helper ==============================================================
def file_path(name: str) -> str:
    """Return absolute path on Desktop for a given filename (secured)."""
    return os.path.join(DESKTOP, secure_filename(name))

# === routes ==============================================================

# Home page  →  serves index.html that lives in the same folder as this script
@app.route("/")
def home():
    base_dir = os.path.dirname(__file__)
    return send_from_directory(base_dir, "index.html")

# Upload a file
@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f or f.filename == "":
        return {"error": "no file provided"}, 400
    f.save(file_path(f.filename))
    return {"msg": "saved", "name": f.filename}

# List files
@app.route("/files", methods=["GET"])
def list_files():
    files = [fn for fn in os.listdir(DESKTOP) if os.path.isfile(file_path(fn))]
    return jsonify(files)

# Download a file
@app.route("/files/<path:filename>", methods=["GET"])
def download(filename):
    return send_from_directory(DESKTOP, filename, as_attachment=True)

# Delete a file
@app.route("/files/<path:filename>", methods=["DELETE"])
def delete(filename):
    try:
        os.remove(file_path(filename))
        return {"msg": "deleted"}
    except FileNotFoundError:
        abort(404)

# === run ================================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
