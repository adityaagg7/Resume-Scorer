import re
import requests
import os
import pymongo
from difflib import get_close_matches
import pdfplumber
from docx import Document
import json

# --- Mongo Setup ---
client = pymongo.MongoClient("mongodb://admin:123@localhost:27017/?authSource=admin")
db = client["resume"]
sections_collection = db["resume-sections"]

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "mistral"


# --- Load sections + aliases ---
def load_sections():
    sections_collection.find().sort('optional')
    sections = []
    for doc in sections_collection.find():
        sections.append(doc["title"].lower())

    return sections

sections = load_sections()

def parse_resume_sections_llm(resume_text: str) -> dict:
    prompt = f"""
You are a professional resume parser.

Below is the full text of a resume. Identify and extract the following sections:
{sections}

For each section you find, return a JSON key with the section ID and its full content.
If a section is not present, you may omit it. DONOT CHANGE RESUME TEXT CONTENT.

Resume:
\"\"\"
{resume_text}
\"\"\"

Respond ONLY with valid JSON
"sectionName1":"Content1",
"sectionName2":"Content2".....
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        print("sending request")
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()["response"]

        # Try parsing response content as JSON
        print("got json")
        parsed_json = json.loads(result)
        return parsed_json

    except requests.exceptions.RequestException as e:
        print(f"HTTP Error: {e}")
    except json.JSONDecodeError:
        print("LLM response was not valid JSON:")
        print(result)

    return {}



# --- Normalize lines ---
def normalize_line(line):
    return re.sub(r"[^a-zA-Z0-9\s]", "", line).strip().lower()


# --- Text Extracter ---
def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                
                for character in page.chars:
                    character["text"]
                text += page.extract_text() + "\n"
                page.close()
        
        # print(text)
        return text
 
    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        raise ValueError(f"Unsupported file type: {ext}")

# --- Main Parser ---
def extract_sections_from_resume(text):
    identifiedSections = {}
    sections.append("unclassified")
    # identifiedSections = parse_resume_sections_llm(text)
    return identifiedSections    
