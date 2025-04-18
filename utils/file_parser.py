import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    document = docx.Document(file.file)
    return "\n".join([para.text for para in document.paragraphs])
