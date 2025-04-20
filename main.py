from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from utils.file_parser import extract_text_from_pdf, extract_text_from_docx
from utils.ai_utils import analyze_student_text, teach_me_subject
from utils.ai_quiz import generate_quiz_from_text  # ✅ FIXED

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/tools", response_class=HTMLResponse)
async def tools(request: Request):
    return templates.TemplateResponse("tools.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, subject: str = Form(...), file: UploadFile = File(...)):
    try:
        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(file)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(file)
        else:
            return templates.TemplateResponse("tools.html", {"request": request, "error": "Unsupported file type"})

        quiz = generate_quiz_from_text(text, subject)
        return templates.TemplateResponse("quiz.html", {"request": request, "quiz": quiz})

    except Exception as e:
        print("Quiz error:", str(e))
        return templates.TemplateResponse("tools.html", {"request": request, "error": "An error occurred in quiz generation."})


@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, chat_file: UploadFile = File(...), question: str = Form(...), subject: str = Form(...)):
    try:
        if chat_file.content_type == "application/pdf":
            text = extract_text_from_pdf(chat_file)
        elif chat_file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(chat_file)
        else:
            return templates.TemplateResponse("tools.html", {"request": request, "error": "Unsupported file type"})

        answer = teach_me_subject(subject, f"Leçon:\n{text}\n\nQuestion:\n{question}")
        return templates.TemplateResponse("tools.html", {"request": request, "chat_response": answer})

    except Exception as e:
        print("Chat error:", str(e))
        return templates.TemplateResponse("tools.html", {"request": request, "error": "An error occurred while answering your question."})


@app.post("/canevas", response_class=HTMLResponse)
async def canevas(request: Request, text: str = Form(...)):
    try:
        feedback = analyze_student_text(text)
        return templates.TemplateResponse("tools.html", {"request": request, "canevas_feedback": feedback})
    except Exception as e:
        print("Canevas error:", str(e))
        return templates.TemplateResponse("tools.html", {"request": request, "error": "An error occurred in text analysis."})
