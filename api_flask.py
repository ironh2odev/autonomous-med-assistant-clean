# api_flask.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from vision.models.vit_dummy import diagnose_image as vit_diagnose_image
from PIL import UnidentifiedImageError
from datetime import datetime
import os
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains and routes

# Ensure necessary folders and files
os.makedirs("data", exist_ok=True)
log_path = os.path.join("data", "diagnosis_log.csv")
if not os.path.exists(log_path):
    df = pd.DataFrame(columns=["timestamp", "diagnosis", "confidence", "image_path"])
    df.to_csv(log_path, index=False)

@app.route("/diagnose", methods=["POST"])
def diagnose():
    print("🔔 Diagnose endpoint hit.")

    if "file" not in request.files:
        print("❌ No file found in request.")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    print(f"📸 Received file: {file.filename}")

    try:
        # Auto timestamp image saves
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join("data", f"xray_{timestamp}.png")
        file.save(image_path)
        print(f"💾 Saved file to: {image_path}")

        # Run diagnosis using cached model
        result = vit_diagnose_image(image_path)

        # Save result to CSV log
        new_row = pd.DataFrame({
            "timestamp": [timestamp],
            "diagnosis": [result["diagnosis"]],
            "confidence": [result["confidence"]],
            "image_path": [image_path]
        })
        log_df = pd.read_csv(log_path)
        log_df = pd.concat([log_df, new_row], ignore_index=True)
        log_df.to_csv(log_path, index=False)

        print(f"✅ Diagnosis completed and saved: {result}")
        return jsonify(result)

    except UnidentifiedImageError as e:
        print(f"❌ PIL Error: {e}")
        return jsonify({"error": "Invalid image file"}), 400

    except Exception as e:
        print(f"🔥 Unexpected Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(debug=True)
