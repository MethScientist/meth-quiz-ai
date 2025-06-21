import os
from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import shutil
import fitz  # PyMuPDF

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Subject roles
def get_subject_roles():
    return {
        "français": "Tu es un professeur de français.",
        "anglais": "You are an English teacher.",
        "arabe": "أنت أستاذ في اللغة العربية.",
        "espagnol": "Eres un profesor de español.",
        "allemand": "Du bist ein Deutschlehrer.",
        "mathématique": "Tu es un professeur de mathématiques.",
        "physique": "Tu es un professeur de physique.",
        "svt": "Tu es un professeur de sciences de la vie et de la terre.",
        "histoire": "Tu es un professeur d'histoire.",
        "géographie": "Tu es un professeur de géographie.",
        "emc": "Tu es un professeur d'Enseignement Moral et Civique.",
        "enseignement_scientifique_physique": "Tu es un professeur de la partie physique de l'enseignement scientifique.",
        "enseignement_scientifique_science": "Tu es un professeur de la partie sciences naturelles de l'enseignement scientifique."
    }

# AI chat interaction
def chat_with_ai(system_role, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Generate quiz from text
def generate_quiz_from_text(text: str) -> str:
    prompt = (
        "Génère un quiz de 3 questions à choix multiples à partir du texte suivant :\n\n"
        f"{text}\n\n"
        "Chaque question doit avoir une seule bonne réponse et trois distracteurs."
    )
    return chat_with_ai("Tu es un assistant pédagogique.", prompt)

# Generate notes and exercises from lesson
def generate_notes_and_exercises(lesson_text):
    prompt = f"""
Tu es un assistant éducatif. À partir du texte de la leçon suivant, génère :
1. Des notes d'étude concises
2. Trois exercices
3. Les solutions des exercices

Leçon :
{lesson_text}

## Notes
## Exercices
## Solutions
"""
    return chat_with_ai("Assistant éducatif", prompt)

# Extract text from uploaded PDF
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def process_chat(subject: str = Form(...), text: str = Form(...)):
    role = get_subject_roles().get(subject, "Tu es un professeur expert.")
    answer = chat_with_ai(role, text)
    return JSONResponse({"response": answer})

@app.post("/upload")
def upload_file(subject: str = Form(...), file: UploadFile = Form(...)):
    file_location = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_location)
    role = get_subject_roles().get(subject, "Tu es un professeur expert.")
    summary = chat_with_ai(role, extracted_text)

    return JSONResponse({"summary": summary, "extracted_text": extracted_text})

@app.post("/quiz")
def create_quiz(text: str = Form(...)):
    quiz = generate_quiz_from_text(text)
    return JSONResponse({"quiz": quiz})

@app.post("/notes")
def create_notes(text: str = Form(...)):
    content = generate_notes_and_exercises(text)
    return JSONResponse({"content": content})
