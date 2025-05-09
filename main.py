# main_app.py
from fastapi import FastAPI, Request, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import openai, os
from dotenv import load_dotenv
from utils.ai_utils import generate_quiz_from_text, teach_me_subject
from utils.file_parser import extract_text_from_pdf, extract_text_from_docx
from sqlmodel import SQLModel, Field, Session, create_engine, select

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Database models
database_url = "sqlite:///./edu_site.db"
engine = create_engine(database_url, echo=False)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    subject: str
    lesson: str
    content: str

# Create tables
SQLModel.metadata.create_all(engine)

# Auth utils
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_user_by_email(email: str):
    with Session(engine) as session:
        return session.exec(select(User).where(User.email == email)).first()

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

# App setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Routes
def init_app():
    pass

@app.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    if get_user_by_email(form_data.username):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=form_data.username, hashed_password=get_password_hash(form_data.password))
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/subjects")
async def list_subjects(current_user: User = Depends(get_current_user)):
    # Example static list; replace with DB or config
    return ["maths", "physics", "french", "english"]

@app.post("/generate_quiz")
async def generate_quiz(data: dict, current_user: User = Depends(get_current_user)):
    text = data.get("text")
    subject = data.get("subject")
    quiz = generate_quiz_from_text(text, subject)
    return {"quiz": quiz}

@app.post("/notes")
async def save_note(data: dict, current_user: User = Depends(get_current_user)):
    note = Note(user_id=current_user.id, subject=data.get("subject"), lesson=data.get("lesson"), content=data.get("content"))
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
    return {"id": note.id}

@app.get("/notes")
async def get_notes(subject: Optional[str] = None, lesson: Optional[str] = None, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        query = select(Note).where(Note.user_id == current_user.id)
        if subject:
            query = query.where(Note.subject == subject)
        if lesson:
            query = query.where(Note.lesson == lesson)
        results = session.exec(query).all()
    return results

# Static pages
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Mount your existing routes (chatbot, upload_file, etc.)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_app:app", host="0.0.0.0", port=10000, reload=True)