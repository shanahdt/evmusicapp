import json
import os
from datetime import datetime, timezone

from flask import Flask, abort, jsonify, redirect, render_template, request, send_from_directory, url_for

app = Flask(__name__)

TEMPLATES_EXPERIMENTS_DIR = os.path.join(os.path.dirname(__file__), "templates", "experiments")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Define custom titles and descriptions for each experiment
EXPERIMENT_METADATA = {
    "king_song_type_diagnosticity": {
        "title": "Disney Categorization",
        "description": "Listen to and compare music from Disney and other musicals.",
    },
    "oesterheld_camps_timbre_descriptions": {
        "title": "Describing Musical Sounds",
        "description": "Listen to a sound and rank timbral descriptions.",
    },
}


def get_experiment_metadata(experiment_id, relative_dir):
    candidates = []
    if experiment_id:
        candidates.append(experiment_id)

    if relative_dir and relative_dir != ".":
        candidates.append(relative_dir)
        candidates.append(relative_dir.replace(os.sep, "/"))

    for candidate in candidates:
        if candidate in EXPERIMENT_METADATA:
            return EXPERIMENT_METADATA[candidate]

    return {}


def discover_experiments():
    experiments = []

    if not os.path.isdir(TEMPLATES_EXPERIMENTS_DIR):
        return experiments

    for root, _, files in os.walk(TEMPLATES_EXPERIMENTS_DIR):
        html_files = sorted(
            filename for filename in files if filename.endswith(".html")
        )

        for filename in html_files:
            experiment_id = os.path.splitext(filename)[0]
            relative_dir = os.path.relpath(root, TEMPLATES_EXPERIMENTS_DIR)
            template_dir = os.path.join("experiments", relative_dir).replace(os.sep, "/")
            template_path = os.path.join(template_dir, filename).replace(os.sep, "/")

            if relative_dir == ".":
                template_dir = "experiments"
                template_path = os.path.join("experiments", filename).replace(os.sep, "/")

            metadata = get_experiment_metadata(experiment_id, relative_dir)
            title = metadata.get("title", experiment_id.replace("_", " ").title())
            description = metadata.get("description", f"Experiment found in {relative_dir or 'root'}")

            experiments.append(
                {
                    "id": experiment_id,
                    "title": title,
                    "description": description,
                    "template": template_path,
                    "template_dir": template_dir,
                }
            )

    return experiments


def get_experiments():
    return discover_experiments()


def get_experiment(experiment_id):
    experiments = get_experiments()
    return next((e for e in experiments if e["id"] == experiment_id), None)


@app.route("/")
def index():
    return render_template("index.html", experiments=get_experiments())


@app.route("/<experiment_id>")
def experiment_redirect(experiment_id):
    exp = get_experiment(experiment_id)
    if exp is None:
        return render_template("404.html"), 404
    return redirect(url_for("experiment", experiment_id=experiment_id))


@app.route("/<experiment_id>/")
def experiment(experiment_id):
    exp = get_experiment(experiment_id)
    if exp is None:
        return render_template("404.html"), 404
    return render_template(exp["template"], experiment=exp)


@app.route("/<experiment_id>/<path:resource_path>")
def experiment_resource(experiment_id, resource_path):
    exp = get_experiment(experiment_id)
    if exp is None:
        return render_template("404.html"), 404

    asset_folder = os.path.join(os.path.dirname(__file__), "templates", exp["template_dir"])
    return send_from_directory(asset_folder, resource_path)


@app.route("/save", methods=["POST"])
def save_data():
    payload = request.get_json(silent=True)
    if payload is None:
        app.logger.warning("Save request contained invalid JSON from %s", request.remote_addr)
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    experiment_id = payload.get("experiment_id", "unknown")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    filename = f"{experiment_id}_{timestamp}.json"
    
    # Create experiment-specific folder within data 
    experiment_dir = os.path.join(DATA_DIR, experiment_id)
    os.makedirs(experiment_dir, exist_ok=True)
    
    filepath = os.path.join(experiment_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    return jsonify({"status": "ok", "file": filename})


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
