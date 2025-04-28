# api/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from vision.models.inference import diagnose_image
import os
import csv
from datetime import datetime

# === App Initialization ===
app = FastAPI(
    title="Autonomous AI Medical Assistant",
    description="API for diagnosing X-rays and consulting symptoms.",
    version="1.0.0",
)

# === CORS Configuration (Frontend <-> Backend) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can later restrict this to specific domains (recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Constants ===
DATA_DIR = "data/uploads"
LOG_FILE = "data/diagnosis_log.csv"

# Ensure necessary directories exist
os.makedirs(DATA_DIR, exist_ok=True)

# === Routes ===

@app.get("/")
def root():
    return {"message": "Welcome to the Autonomous AI Medical Assistant API!"}


@app.post("/diagnose")
async def diagnose(file: UploadFile = File(...)):
    """
    Accepts an uploaded X-ray image and returns a diagnosis.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"xray_{timestamp}.png"
    file_path = os.path.join(DATA_DIR, filename)

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        return {"error": f"Failed to save uploaded file: {str(e)}"}

    # Run AI diagnosis
    try:
        result = diagnose_image(file_path)
    except Exception as e:
        return {"error": f"Failed to diagnose image: {str(e)}"}

    # Log the result
    try:
        with open(LOG_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            if f.tell() == 0:  # New file, write headers
                writer.writerow(["filename", "diagnosis", "confidence", "timestamp", "image_path"])
            writer.writerow([
                filename,
                result["diagnosis"],
                result["confidence"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                file_path
            ])
    except Exception as e:
        print(f"[ERROR] Failed to log diagnosis: {e}")

    return result
