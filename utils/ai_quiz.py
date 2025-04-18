import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("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")

def generate_quiz_from_text(text):
    prompt = f"Generate a quiz with 5 multiple-choice questions based on the following lesson:\n\n{text}\n\nFormat the quiz nicely."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful quiz generator."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

