import os

from flask import Flask, send_from_directory

# This site is a static site (deployed via GitHub Pages) that saves
# experiment data directly to OSF via DataPipe (https://pipe.jspsych.org).
# app.py is only a convenience server for previewing it locally -- it
# just serves the repo root the same way GitHub Pages would.

app = Flask(__name__, static_folder=None)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return send_from_directory(ROOT_DIR, "index.html")


@app.route("/<path:path>")
def serve(path):
    full_path = os.path.join(ROOT_DIR, path)

    if os.path.isdir(full_path):
        if os.path.isfile(os.path.join(full_path, "index.html")):
            return send_from_directory(full_path, "index.html")
        return render_404()

    if os.path.isfile(full_path):
        return send_from_directory(ROOT_DIR, path)

    return render_404()


def render_404():
    return send_from_directory(ROOT_DIR, "404.html"), 404


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
