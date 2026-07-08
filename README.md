# evmusicapp

Experiment website for the Noise Lab. This is a static site (deployable on
GitHub Pages) — there is no backend. Each experiment saves its data directly
to OSF via [DataPipe](https://pipe.jspsych.org).

## Structure

```
index.html                   home page / experiment list
404.html
css/, images/, js/, midi/    shared static assets
experiments/<experiment_id>/index.html   one static page per experiment
```

Every path inside an experiment page is relative (e.g. `../../css/style.css`),
so the site works the same whether it's served from a domain root or from a
GitHub Pages project subpath.

## Local preview

`app.py` is a thin Flask server used only to preview the site locally — it
just serves the repo root the same way GitHub Pages would (it is not a data
backend).

```
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000/.

## Deploying to GitHub Pages

In the repo settings, under **Pages**, set the source to the `main` branch,
root folder (`/`). GitHub Pages will then serve `index.html` and `404.html`
directly.

## Saving data to OSF via DataPipe

Each experiment page (`experiments/*/index.html`) posts its data to
[pipe.jspsych.org](https://pipe.jspsych.org), which forwards it to an OSF
project you control. To wire up a new or existing experiment:

1. Create an OSF project (or use an existing one) at osf.io.
2. Sign in to [pipe.jspsych.org](https://pipe.jspsych.org) with your OSF
   account and link it if prompted.
3. Click **New Experiment**, give it a title, and point it at your OSF
   project ID (the short code in your OSF project's URL) — DataPipe will
   create a component under that project to store the files.
4. On the experiment's dashboard, turn on **"Enable data collection"** (this
   step is required — the pipe silently rejects data until it's enabled).
5. Copy the experiment ID DataPipe gives you and paste it into the matching
   `DATAPIPE_EXPERIMENT_ID` constant near the top of that experiment's
   `<script>` block in `experiments/<experiment_id>/index.html`.

Each experiment currently has `DATAPIPE_EXPERIMENT_ID` set to a placeholder
(`PASTE_YOUR_DATAPIPE_EXPERIMENT_ID_HERE`) — data won't be saved until that's
replaced with a real ID. Filenames are generated per-submission
(`<experiment_id>_<participant_id>_<timestamp>_<random>.json`) since DataPipe
rejects duplicate filenames.

`gather_timbre_responses.py` still processes local JSON dumps in `data/` —
now that saving goes straight to OSF, you'll need to download the response
files from your OSF project into `data/` before running it.
