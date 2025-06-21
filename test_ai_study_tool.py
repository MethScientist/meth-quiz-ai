import os
import openai
from dotenv import load_dotenv
from utils.file_parser import read_lesson_file

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_notes_and_exercises(lesson_text):
    prompt = f"""
You are an AI teacher assistant. Read the following lesson and:
- Summarize the key points as notes
- Create 3 exercises
- Provide solutions to each exercise

Lesson:
{lesson_text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000
    )

    return response.choices[0].message.content

def process_file(file_path):
    lesson_text = read_lesson_file(file_path)
    return generate_notes_and_exercises(lesson_text)

if __name__ == "__main__":
    file_path = "utils/lesson_files/sample_lesson.txt"
    output = process_file(file_path)
    print(output)
