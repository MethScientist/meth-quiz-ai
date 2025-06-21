from utils.file_parser import read_lesson_file
from utils.ai_utils import generate_notes_and_exercises

def process_file(file_path):
    lesson_text = read_lesson_file(file_path)
    return generate_notes_and_exercises(lesson_text)

if __name__ == "__main__":
    file_path = "utils/lesson_files/sample_lesson.pdf"  # Your test file
    output = process_file(file_path)
    print(output)

