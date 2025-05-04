# api/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vision.models.inference import diagnose_image
from utils.medical_agent import consult_symptoms, check_drug_interactions
import os
import csv
from datetime import datetime
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = os.getenv("UPLOAD_DIR", "data/uploads")
LOG_FILE = os.getenv("LOG_FILE", "data/diagnosis_log.csv")
os.makedirs(DATA_DIR, exist_ok=True)

app = FastAPI(
    title="Autonomous AI Medical Assistant",
    description="API for diagnosing X-rays, consulting symptoms, and checking drug interactions.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomsInput(BaseModel):
    symptoms: str

class DrugCheckInput(BaseModel):
    drug_ids: List[int]

@app.get("/")
def root():
    return {"message": "Welcome to the Autonomous AI Medical Assistant API!"}

@app.post("/diagnose")
async def diagnose(file: UploadFile = File(...)):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"xray_{timestamp}.png"
    file_path = os.path.join(DATA_DIR, filename)

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        return {"error": str(e)}

    try:
        result = diagnose_image(file_path)
    except Exception as e:
        logger.error(f"Diagnosis error: {e}")
        return {"error": str(e)}

    try:
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(["filename", "diagnosis", "confidence", "timestamp", "image_path"])
            writer.writerow([
                filename,
                result["diagnosis"],
                result["confidence"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                file_path
            ])
    except Exception as e:
        logger.warning(f"Could not log diagnosis: {e}")

    return result

@app.post("/consult")
def consult(input: SymptomsInput):
    try:
        output = consult_symptoms(input.symptoms)
    except Exception as e:
        logger.error(f"Consultation error: {e}")
        return {"error": str(e)}
    return {"consultation": output}

@app.post("/check-drug-safety")
def check_safety(input: DrugCheckInput):
    try:
        results = check_drug_interactions(input.drug_ids)
    except Exception as e:
        logger.error(f"Interaction check error: {e}")
        return {"error": str(e)}
    return {"interactions": results}

@app.delete("/delete-diagnosis")
def delete_diagnosis(filename: str):
    """Delete a diagnosis record by filename from log and delete file."""
    try:
        rows = []
        with open(LOG_FILE, "r") as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader if row["filename"] != filename]
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["filename", "diagnosis", "confidence", "timestamp", "image_path"])
            writer.writeheader()
            writer.writerows(rows)
        file_path = os.path.join(DATA_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        return {"status": "deleted", "filename": filename}
    except Exception as e:
        logger.error(f"Delete error: {e}")
        return {"error": str(e)}