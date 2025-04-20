# utils/ai_utils.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

subject_roles = {
    "maths": "Tu es un professeur de mathématiques...",
    "physics": "Tu es un professeur de physique...",
    "french": "Tu es un professeur de français...",
    "english": "You are an English teacher...",
    # add all subjects here
}


def teach_me_subject(subject, text_or_question):
    role = subject_roles.get(subject, "Tu es un professeur expert.")

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": text_or_question}
        ]
    )
    return response.choices[0].message.content.strip()


def analyze_student_text(text):
    prompt = f"Voici le texte écrit par l'élève :\n\n{text}\n\nDonne un retour constructif."
    return chat_with_ai("Tu es un professeur qui corrige les textes.", prompt)


def chat_with_ai(system_role, prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_quiz_from_text(text):
    prompt = (
        "You are a helpful assistant that generates multiple-choice questions.\n"
        "Create a quiz with 5 questions based on the following text. Each question should have 4 options, and indicate the correct answer.\n\n"
        f"Text:\n{text}\n\n"
        "Format:\n"
        "Q1: ...?\nA. ...\nB. ...\nC. ...\nD. ...\nAnswer: ...\n\n"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']