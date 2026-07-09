# Student Report Helper

A Flask web app for generating one Word progress report per pupil from:

- a Word report template (`.docx`)
- an attendance spreadsheet (`.xlsx`)
- an attainment tracker (`.xlsx`)

The app preserves the Word template layout by editing the relevant tables directly.

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Deploy On Render

Render's Flask quickstart uses:

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

This project also includes `render.yaml`, so Render can create the web service from the repository settings.

Recommended Render settings:

- Service type: Web Service
- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Health check path: `/health`

After deployment, Render will provide an `onrender.com` link that teachers can use.

## Data Privacy Note

Uploaded files are processed in a temporary folder and returned as a ZIP download. The app does not intentionally store pupil data between requests. For real school use, keep the GitHub repository private and use a Render plan/settings appropriate for pupil data.

## Known Data Checks

The app adds a `generation_summary.txt` file to the ZIP if any pupils are missing attendance or attainment data.
