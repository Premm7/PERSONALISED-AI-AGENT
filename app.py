# app.py
from flask import Flask, request, jsonify, render_template, send_file
from assistant_core import Assistant
from scheduler import start as start_scheduler
from dotenv import load_dotenv
import tempfile
import pyttsx3
import os

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
assistant = Assistant()

# Start background reminder scheduler
start_scheduler()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/command", methods=["POST"])
def api_command():
    data = request.get_json() or {}
    text = data.get("text", "")
    res = assistant.handle(text)
    return jsonify(res)

@app.route("/api/tts", methods=["POST"])
def api_tts():
    data = request.get_json() or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    engine = pyttsx3.init()
    fd, filename = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return send_file(filename, as_attachment=True, download_name="tts.mp3")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
