import json
import os
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

EXPERIMENTS = [
    {
        "id": "tone_discrimination",
        "title": "Tone Discrimination",
        "description": "Identify whether two tones are the same or different.",
    },
    {
        "id": "melody_recognition",
        "title": "Melody Recognition",
        "description": "Listen to a melody and indicate whether you have heard it before.",
    },
]

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html", experiments=EXPERIMENTS)


@app.route("/experiment/<experiment_id>")
def experiment(experiment_id):
    exp = next((e for e in EXPERIMENTS if e["id"] == experiment_id), None)
    if exp is None:
        return render_template("404.html"), 404
    return render_template(f"experiments/{experiment_id}.html", experiment=exp)


@app.route("/save", methods=["POST"])
def save_data():
    payload = request.get_json(silent=True)
    if payload is None:
        app.logger.warning("Save request contained invalid JSON from %s", request.remote_addr)
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    experiment_id = payload.get("experiment_id", "unknown")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    filename = f"{experiment_id}_{timestamp}.json"
    filepath = os.path.join(DATA_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    return jsonify({"status": "ok", "file": filename})


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
