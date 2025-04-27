# api/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from vision.models.inference import diagnose_image
import os, csv
from datetime import datetime

# === App Init ===
app = FastAPI()

# === CORS (Frontend <-> Backend) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Constants ===
DATA_DIR = "data/uploads"
LOG_FILE = "data/diagnosis_log.csv"
os.makedirs(DATA_DIR, exist_ok=True)

# === Routes ===
@app.post("/diagnose")
async def diagnose(file: UploadFile = File(...)):
    # Save uploaded file (✅ Fix: use await file.read())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"xray_{timestamp}.png"
    file_path = os.path.join(DATA_DIR, filename)

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        return {"error": f"Failed to save file: {str(e)}"}

    # Run diagnosis
    result = diagnose_image(file_path)

    # Log the result
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
        print(f"[ERROR] Could not write to log: {e}")

    return result
