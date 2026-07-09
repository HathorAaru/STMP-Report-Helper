from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

import os

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from report_helper.report_builder import generate_zip


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_UPLOAD_MB", "32")) * 1024 * 1024


def _save_upload(upload, folder, fallback_name):
    filename = secure_filename(upload.filename or fallback_name)
    path = Path(folder) / filename
    upload.save(path)
    return path


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate():
    required_files = ["template", "attendance", "attainment"]
    missing = [field for field in required_files if field not in request.files or not request.files[field].filename]
    class_name = request.form.get("class_name", "").strip()
    teacher_name = request.form.get("teacher_name", "").strip()

    if missing or not class_name or not teacher_name:
        return render_template(
            "index.html",
            error="Please add the template, attendance, tracker, class, and teacher before generating reports.",
        ), 400

    with TemporaryDirectory() as temp_dir:
        template_path = _save_upload(request.files["template"], temp_dir, "template.docx")
        attendance_path = _save_upload(request.files["attendance"], temp_dir, "attendance.xlsx")
        attainment_path = _save_upload(request.files["attainment"], temp_dir, "attainment.xlsx")
        zip_path = Path(temp_dir) / "Student Reports.zip"

        try:
            _, warnings = generate_zip(
                template_path,
                attendance_path,
                attainment_path,
                zip_path,
                class_name=class_name,
                teacher_name=teacher_name,
            )
        except Exception as exc:
            return render_template("index.html", error=str(exc)), 400

        payload = BytesIO(zip_path.read_bytes())
        payload.seek(0)
        return send_file(
            payload,
            as_attachment=True,
            download_name="Student Reports.zip",
            mimetype="application/zip",
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
