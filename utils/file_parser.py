# utils/file_parser.py
import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file):
    try:
        doc = fitz.open(stream=file.file.read(), filetype="pdf")
        return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_docx(file):
    try:
        document = docx.Document(file.file)
        return "\n".join(para.text for para in document.paragraphs)
    except Exception as e:
        return f"Error reading DOCX: {e}"
