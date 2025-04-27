# scripts/reset_logs.py

import os
import shutil

# Paths
log_path = "data/diagnosis_log.csv"
upload_folder = "data/uploads"

# Delete diagnosis log file
if os.path.exists(log_path):
    os.remove(log_path)
    print(f"Deleted: {log_path}")
else:
    print("No diagnosis_log.csv found.")

# Clear uploads folder
if os.path.exists(upload_folder):
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
else:
    print("Uploads folder not found.")
