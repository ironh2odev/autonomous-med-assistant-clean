# 🩺 Autonomous AI Medical Diagnosis Assistant

An AI-powered medical assistant that analyzes chest X-rays, provides symptom consultations, and checks drug interactions—all in one app.

## 🚀 Features

✅ Upload chest X-ray images and receive AI-generated diagnoses  
✅ Symptom consultation using GPT-based medical assistant  
✅ Drug interaction checker powered by Graph Neural Networks  
✅ View, download, and delete diagnosis history  
✅ Clean Streamlit front-end + FastAPI back-end  
✅ Ready for deployment on Railway / Render / AWS

---

## 🏗️ Tech Stack

| Layer            | Tech                      |
|-----------------|--------------------------|
| Front-End        | Streamlit                |
| Back-End         | FastAPI                  |
| AI Models        | Vision Transformer (ViT), GPT-4, GNN (DGL) |
| Infrastructure   | Docker, Railway          |
| Data Logging     | CSV (pandas)             |

---

## 📦 Installation

1️⃣ Clone the repo:

```bash
git clone https://github.com/ironh2odev/ai-medical-assistant.git
cd ai-medical-assistant

2️⃣ Create a virtual environment:
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

3️⃣ Install dependencies:
pip install -r requirements.txt

4️⃣ Create a .env file:
OPENAI_API_KEY=your-key-here
API_URL=http://localhost:8000
BACKEND_URL=http://localhost:8000/diagnose
API_CONSULT_URL=http://localhost:8000/consult
API_CHECK_DRUG_URL=http://localhost:8000/check-drug-safety
LOG_FILE=data/diagnosis_log.csv

5️⃣ Run the backend (FastAPI):
uvicorn api.main:app --reload --port 8000

6️⃣ Run the frontenf (Streamlit):
streamlit run ui/app.py
