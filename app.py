from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils.video_tools import convert_to_sticker
import os
import uuid

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "Nessun file 'video' nel form-data"}), 400

    video = request.files["video"]
    if video.filename == "":
        return jsonify({"error": "Nessun file selezionato"}), 400

    file_id = str(uuid.uuid4())[:8]
    in_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_{video.filename}")
    video.save(in_path)

    out_path = os.path.join(OUTPUT_FOLDER, f"{file_id}_sticker.webm")
    try:
        convert_to_sticker(in_path, out_path)
    except Exception as e:
        return jsonify({"error": f"Errore conversione: {e}"}), 500

    return send_file(out_path, as_attachment=True, download_name="sticker.webm", mimetype="video/webm")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
