# api/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vision.models.inference import diagnose_image
from utils.medical_agent import consult_symptoms
from datetime import datetime
import os

# In-memory store
diagnosis_log = []

app = FastAPI(
    title="🩺 Autonomous AI Medical Assistant",
    description="🩻 Diagnose X-rays and consult symptoms.",
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://autonomous-med-assistant-frontend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomsInput(BaseModel):
    symptoms: str

@app.get("/")
def root():
    return {"message": "Welcome to the 🩺 Autonomous AI Medical Assistant API!"}

@app.post("/diagnose")
async def diagnose(file: UploadFile = File(...)):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = file.filename

    contents = await file.read()
    file_path = f"data/uploads/{filename}"
    os.makedirs("data/uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(contents)

    result = diagnose_image(file_path)
    record = {
        "filename": filename,
        "diagnosis": result["diagnosis"],
        "confidence": result["confidence"],
        "timestamp": timestamp,
        "image_path": file_path,
    }
    diagnosis_log.append(record)
    return record

@app.get("/diagnosis-log")
def get_diagnosis_log():
    return {"log": diagnosis_log}

@app.post("/consult")
def consult(input: SymptomsInput):
    output = consult_symptoms(input.symptoms)
    return {"consultation": output}

@app.delete("/delete-diagnoses")
def delete_diagnoses():
    diagnosis_log.clear()
    return {"status": "cleared"}
