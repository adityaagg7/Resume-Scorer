from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
import shutil
import os
from resume_scorer import extract_text, score_resume

app = FastAPI()

TEMP_DIR = "./"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/score/")
async def score_resume_endpoint(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        file_location = os.path.join(TEMP_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract and score
        text = extract_text(file_location)
        result = score_resume(text)

        # Cleanup
        os.remove(file_location)

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
