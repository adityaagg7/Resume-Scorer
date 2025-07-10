import os
import pdfplumber
from docx import Document

def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        raise ValueError(f"Unsupported file type: {ext}")

def score_resume(text: str) -> dict:
    score = 0
    comments = []

    word_count = len(text.split())
    if word_count < 150 or word_count > 1500:
        comments.append("Resume should ideally be between 150 and 1500 words.")
    else:
        score += 30

    if "experience" in text.lower():
        score += 20
    else:
        comments.append("Add an 'Experience' section if applicable.")

    if "education" in text.lower():
        score += 20
    else:
        comments.append("Add an 'Education' section if missing.")

    if "skills" in text.lower():
        score += 20
    else:
        comments.append("Mention your 'Skills' clearly.")

    if any(word in text.lower() for word in ["led", "developed", "built", "created"]):
        score += 10
    else:
        comments.append("Use strong action verbs in bullet points.")

    return {
        "score": score,
        "comments": comments
    }
