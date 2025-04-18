from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from utils.file_parser import extract_text_from_pdf, extract_text_from_docx
from utils.ai_quiz import generate_quiz_from_text

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------- ROUTES ----------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/tools", response_class=HTMLResponse)
async def tools(request: Request):
    return templates.TemplateResponse("tools.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, file: UploadFile = File(...)):
    try:
        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(file)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(file)
        else:
            return templates.TemplateResponse("tools.html", {"request": request, "error": "Unsupported file type"})

        quiz = generate_quiz_from_text(text)
        return templates.TemplateResponse("quiz.html", {"request": request, "quiz": quiz})
    except Exception as e:
        print("Error occurred:", str(e))
        return templates.TemplateResponse("tools.html", {"request": request, "error": "An error occurred. Check terminal for details."})

# Basic route to check if app is loading
@app.get("/")
async def home(request: Request):
    print("The server is running!")  # This will appear in the Render logs if it's working
    return HTMLResponse(content="<h1>Server is running!</h1>", status_code=200)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja templates
templates = Jinja2Templates(directory="templates")