import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from docx import Document

def read_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def read_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def read_image(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def read_lesson_file(path):
    path = path.lower()
    if path.endswith(".txt"):
        return read_txt(path)
    elif path.endswith(".pdf"):
        return read_pdf(path)
    elif path.endswith(".docx"):
        return read_docx(path)
    elif path.endswith((".png", ".jpg", ".jpeg")):
        return read_image(path)
    else:
        return "Unsupported file format."
