import pdfplumber
from docx import Document


def read_pdf(path):
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[ERROR] Failed to read PDF: {e}")

    return text


def read_docx(path):
    text = ""
    try:
        doc = Document(path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"[ERROR] Failed to read DOCX: {e}")

    return text


def read_cv(path):
    path = path.lower()

    if path.endswith(".pdf"):
        return read_pdf(path)

    elif path.endswith(".docx"):
        return read_docx(path)

    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX supported.")