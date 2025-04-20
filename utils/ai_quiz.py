import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # ✅ USE SAFE ENV VAR

def generate_quiz_from_text(text, subject):
    role = f"Tu es un professeur de {subject}. Crée un quiz de 5 questions à choix multiples basé sur ce contenu."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": f"Voici le cours :\n\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()
