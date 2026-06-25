from pathlib import Path
from uuid import uuid4

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from services.analyzer import analyze_resume, get_supported_roles, is_supported_role
from services.interview_generator import generate_interview_questions
from services.resume_parser import extract_resume_text, is_allowed_file
from services.roadmap_generator import generate_roadmap


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
MAX_UPLOAD_SIZE_MB = 8


def create_app():
    app = Flask(__name__)

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok", "supported_roles": get_supported_roles()})

    @app.post("/api/analyze")
    def analyze():
        resume_file = request.files.get("resume")
        job_role = _get_form_role()

        if not resume_file or resume_file.filename == "":
            return _error("Resume file is required.", 400)

        if not job_role:
            return _error("Job role is required.", 400)

        if not is_supported_role(job_role):
            return _error(
                "Unsupported job role.",
                400,
                {"supported_roles": get_supported_roles()},
            )

        if not is_allowed_file(resume_file.filename):
            return _error("Invalid file type. Upload a PDF, DOCX, or TXT resume.", 400)

        original_name = secure_filename(resume_file.filename)
        extension = Path(original_name).suffix.lower()
        stored_name = f"{uuid4().hex}{extension}"
        saved_path = UPLOAD_FOLDER / stored_name

        try:
            resume_file.save(saved_path)
            resume_text = extract_resume_text(saved_path)

            if not resume_text.strip():
                return _error("Could not extract text from the resume.", 422)

            return jsonify(analyze_resume(resume_text, job_role))
        except Exception as exc:
            return _error(f"Analysis failed: {exc}", 500)
        finally:
            # Resume files are only needed long enough to parse them.
            if saved_path.exists():
                saved_path.unlink()

    @app.post("/api/interview")
    def interview():
        payload = request.get_json(silent=True) or {}
        job_role = _get_json_role(payload)

        if not job_role:
            return _error("Job role is required.", 400)

        if not is_supported_role(job_role):
            return _error(
                "Unsupported job role.",
                400,
                {"supported_roles": get_supported_roles()},
            )

        return jsonify(generate_interview_questions(job_role))

    @app.post("/api/roadmap")
    def roadmap():
        payload = request.get_json(silent=True) or {}
        job_role = _get_json_role(payload)

        if not job_role:
            return _error("Job role is required.", 400)

        if not is_supported_role(job_role):
            return _error(
                "Unsupported job role.",
                400,
                {"supported_roles": get_supported_roles()},
            )

        missing_skills = payload.get("missing_skills") or payload.get("missingSkills") or []
        if not isinstance(missing_skills, list):
            return _error("missing_skills must be a list.", 400)

        return jsonify(generate_roadmap(job_role, missing_skills))

    @app.errorhandler(413)
    def file_too_large(_):
        return _error(f"File is too large. Limit is {MAX_UPLOAD_SIZE_MB} MB.", 413)

    @app.errorhandler(404)
    def not_found(_):
        return _error("API endpoint not found.", 404)

    return app


def _get_form_role():
    # The current frontend sends "role"; the API also accepts "job_role".
    return (request.form.get("job_role") or request.form.get("role") or "").strip()


def _get_json_role(payload):
    # Support both the requested API field and the existing frontend field.
    return (payload.get("job_role") or payload.get("role") or "").strip()


def _error(message, status_code, extra=None):
    body = {"error": message}
    if extra:
        body.update(extra)
    return jsonify(body), status_code


app = create_app()


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=False)
