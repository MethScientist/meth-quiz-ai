"""
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

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# App setup
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and templates
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ========== ROUTES ==========

@app.get("/chatbot")
def get_chatbot_page(request: Request):
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
        reply = response["choices"][0]["message"]["content"]
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


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = contents.decode("utf-8")
        return JSONResponse(content={"content": text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
"""
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Load templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Home route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})
