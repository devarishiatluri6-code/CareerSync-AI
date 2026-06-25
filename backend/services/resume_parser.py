from pathlib import Path


ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


def is_allowed_file(filename):
    extension = Path(filename).suffix.lower().lstrip(".")
    return extension in ALLOWED_EXTENSIONS


def extract_resume_text(file_path):
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        return _extract_pdf_text(path)

    if extension == ".docx":
        return _extract_docx_text(path)

    if extension == ".txt":
        return _extract_txt_text(path)

    raise ValueError("Unsupported resume file type.")


def _extract_pdf_text(path):
    from PyPDF2 import PdfReader

    reader = PdfReader(str(path))
    page_text = []

    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            page_text.append(text)

    return "\n".join(page_text)


def _extract_docx_text(path):
    from docx import Document

    document = Document(str(path))
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs)


def _extract_txt_text(path):
    return path.read_text(encoding="utf-8", errors="ignore")
