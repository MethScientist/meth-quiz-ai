import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# 📚 Used to explain lessons or answer questions by subject
def teach_me_subject(subject, text_or_question):
    subject_roles = {
        "maths": "Tu es un professeur de mathématiques. Explique les concepts de ce chapitre avec des exemples.",
        "physics": "Tu es un professeur de physique. Simplifie ce contenu avec formules et exemples.",
        "science": "Tu es un professeur de SVT. Résume et explique cette leçon.",
        "history_geo": "Tu es un prof d'histoire-géo. Analyse ce contenu historiquement.",
        "civic": "Tu es un enseignant EMC. Donne une explication claire et structurée.",
        "french": "Tu es un professeur de français. Fais une analyse littéraire de ce texte.",
        "english": "You are an English teacher. Explain this lesson with clear examples.",
        "arabic": "أنت أستاذ لغة عربية. فسر هذا النص بطريقة مبسطة.",
        "spanish": "Eres profesor de español. Explica esta lección en detalle.",
        "scientific": "Tu es un professeur en enseignement scientifique. Détaille les concepts.",
        "philosophy": "Tu es un professeur de philosophie. Propose une analyse et des pistes de réflexion."
    }

    system_msg = subject_roles.get(subject, "Tu es un professeur expert. Explique ce contenu.")

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"{text_or_question}"}
        ]
    )
    return response.choices[0].message.content.strip()


# 🧠 Used for answering direct questions from a lesson
def answer_question_from_text(text, question):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un professeur qui aide à comprendre un document."},
            {"role": "user", "content": f"Voici le contenu de la leçon :\n\n{text}\n\nEt voici la question : {question}"}
        ]
    )
    return response.choices[0].message.content.strip()


# 📝 Used for analyzing student's writing (canevas)
def analyze_student_text(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un professeur qui corrige les textes et donne des conseils de rédaction."},
            {"role": "user", "content": f"Voici le texte écrit par l'élève :\n\n{text}\n\nDonne un retour constructif."}
        ]
    )
    return response.choices[0].message.content.strip()


# 🧪 Optional: Used for quizzes if needed
def generate_quiz_from_text(text, subject):
    role = f"Tu es un professeur de {subject}. Crée un quiz de 5 questions basé sur ce contenu."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": f"Voici le cours :\n\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()
