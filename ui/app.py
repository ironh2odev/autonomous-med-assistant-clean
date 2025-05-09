# ui/app.py

from dotenv import load_dotenv
import os
import sys
import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io

load_dotenv(override=True)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.explainer import explain_diagnosis
from utils.medical_agent import consult_symptoms

API_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/diagnose")
API_CONSULT_URL = os.getenv("API_CONSULT_URL", "http://localhost:8000/consult")
API_LOG_URL = f"{API_BACKEND_URL.rsplit('/',1)[0]}/diagnosis-log"
API_DELETE_URL = f"{API_BACKEND_URL.rsplit('/',1)[0]}/delete-diagnoses"
LOGO_PATH = os.getenv("LOGO_PATH", "assets/logo.png")

st.set_page_config(
    page_title="AI Medical Diagnosis Assistant",
    page_icon="🩺",
    layout="centered"
)

st.sidebar.image(LOGO_PATH, width=100)
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Select a page:",
    ["🩻 Upload X-ray", "📝 Symptom Consultation", "📜 View Past Diagnoses"],
)

if page == "🩻 Upload X-ray":
    st.markdown("## 🩻 Upload X-ray")
    uploaded_file = st.file_uploader("📤 Upload X-ray Image (.png, .jpg, .jpeg)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        file_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        st.image(image, caption="📸 Uploaded X-ray", use_container_width=True)
        st.markdown("### 🔬 Analyzing your X-ray...")

        with st.spinner("Please wait while the AI doctor reviews..."):
            try:
                response = requests.post(API_BACKEND_URL, files={"file": (uploaded_file.name, file_bytes, uploaded_file.type)})
                if response.status_code == 200:
                    result = response.json()
                    st.balloons()
                    st.success("✅ Diagnosis complete!")
                    st.markdown(f"### 🏷️ Diagnosis: `{result['diagnosis']}`")
                    st.info(f"📊 Confidence: `{result['confidence'] * 100:.2f}%`")
                    explanation = explain_diagnosis(result['diagnosis'])
                    st.markdown("### 🧠 Medical Explanation")
                    st.markdown(f"💬 {explanation}")
                else:
                    st.error(f"❌ Backend error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"🚨 Request failed: {e}")

elif page == "📝 Symptom Consultation":
    st.markdown("## 🩺 AI Medical Consultation")
    symptoms = st.text_area("📝 Describe your symptoms:")

    if st.button("🔍 Analyze Symptoms"):
        if symptoms.strip():
            with st.spinner("Analyzing your symptoms..."):
                try:
                    response = requests.post(API_CONSULT_URL, json={"symptoms": symptoms})
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Preliminary medical advice:")
                        st.markdown(f"💬 {result.get('consultation', 'No advice returned.')}")
                    else:
                        st.error(f"❌ Backend error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"🚨 Request failed: {e}")
        else:
            st.warning("⚠️ Please enter some symptoms.")

elif page == "📜 View Past Diagnoses":
    st.markdown("## 📜 Diagnosis History")
    try:
        response = requests.get(API_LOG_URL)
        if response.status_code == 200:
            log_data = response.json().get("log", [])
            if log_data:
                df = pd.DataFrame(log_data)
                st.dataframe(df.drop(columns=["image_path"]))
                selected = st.selectbox("Select timestamp:", df["timestamp"].tolist())
                row = df[df["timestamp"] == selected].iloc[0]
                st.image(row["image_path"], caption=selected, use_container_width=True)

                if st.button("🗑️ Delete All Diagnoses"):
                    requests.delete(API_DELETE_URL)
                    st.warning("🗑️ Diagnosis history cleared.")
                    st.rerun()
            else:
                st.info("🕊️ No diagnoses logged yet.")
        else:
            st.error(f"❌ Backend error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"🚨 Request failed: {e}")
