from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import openai
import os
from dotenv import load_dotenv
from utils.ai_utils import generate_quiz_from_text
from utils.file_parser import extract_text_from_pdf, extract_text_from_docx

# Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# FastAPI app
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static & Template paths
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# ======================= ROUTES ======================= #

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chatbot")
async def get_chatbot_page(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            temperature=0.7,
        )
        reply = response.choices[0].message.content
        return JSONResponse(content={"response": reply})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/generate_quiz")
async def generate_quiz(request: Request):
    data = await request.json()
    text = data.get("text")
    try:
        quiz = generate_quiz_from_text(text)
        return JSONResponse(content={"quiz": quiz})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/upload_lesson")
async def upload_lesson(file: UploadFile = File(...)):
    try:
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_docx(file)
        else:
            contents = await file.read()
            text = contents.decode("utf-8")

        return JSONResponse(content={"content": text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
