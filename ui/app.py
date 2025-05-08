# ui/app.py

from dotenv import load_dotenv
import os
import sys
import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io

# === Load environment variables ===
load_dotenv(override=True)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.explainer import explain_diagnosis
from utils.medical_agent import consult_symptoms

# === Config ===
API_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/diagnose")
API_CONSULT_URL = os.getenv("API_CONSULT_URL", "http://localhost:8000/consult")
API_CHECK_DRUG_URL = os.getenv("API_CHECK_DRUG_URL", "http://localhost:8000/check-drug-safety")
LOG_FILE = os.getenv("LOG_FILE", "data/diagnosis_log.csv")
LOGO_PATH = os.getenv("LOGO_PATH", "assets/logo.png")

st.set_page_config(
    page_title="AI Medical Diagnosis Assistant",
    page_icon="🩺",
    layout="centered"
)

st.sidebar.image(LOGO_PATH, width=100)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Select a page:",
    ["🩻 Upload X-ray", "📝 Symptom Consultation", "📜 View Past Diagnoses"],
)

st.sidebar.markdown(f"📍 **Current Page:** {page}")

if page == "🩻 Upload X-ray":
    st.markdown("<h1 style='text-align: center;'>🩻 Autonomous AI Medical Diagnosis Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload a chest X-ray image to receive an AI-generated diagnosis.</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📤 Upload X-ray Image (.png, .jpg, .jpeg)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        file_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        st.image(image, caption="📸 Uploaded X-ray", use_container_width=True)

        st.divider()
        st.markdown("<h3 style='text-align: center;'>🔬 Analyzing your X-ray...</h3>", unsafe_allow_html=True)

        with st.spinner("Please wait while the AI doctor reviews..."):
            try:
                response = requests.post(API_BACKEND_URL, files={"file": (uploaded_file.name, file_bytes, uploaded_file.type)})

                if response.status_code == 200:
                    result = response.json()
                    st.balloons()
                    st.success("✅ Diagnosis complete!")

                    st.markdown(f"### 🏷️ **Diagnosis:** `{result['diagnosis']}`")
                    st.info(f"📊 **Confidence:** `{result['confidence'] * 100:.2f}%`")

                    if "note" in result:
                        st.markdown(f"🩺 _Doctor’s Note:_ {result['note']}")

                    st.divider()
                    st.markdown("### 🧠 Medical Explanation")

                    with st.spinner("Summarizing in simple language..."):
                        explanation = explain_diagnosis(result['diagnosis'])
                        st.markdown(f"💬 _{explanation}_")

                    st.divider()
                    if st.button("📤 Upload Another X-ray"):
                        st.rerun()

                else:
                    st.error(f"❌ Backend error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"🚨 Request failed: {e}")

elif page == "📝 Symptom Consultation":
    st.markdown("<h1 style='text-align: center;'>🩺 AI Medical Consultation</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Describe your symptoms for preliminary advice (⚠️ does not replace a doctor).</p>", unsafe_allow_html=True)

    symptoms = st.text_area("📝 Describe your symptoms:")

    if st.button("🔍 Analyze Symptoms"):
        if symptoms.strip() == "":
            st.warning("⚠️ Please enter some symptoms.")
        else:
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

elif page == "📜 View Past Diagnoses":
    st.markdown("<h1 style='text-align: center;'>📜 Diagnosis History</h1>", unsafe_allow_html=True)

    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)

        if not df.empty:
            if "image_path" in df.columns:
                st.dataframe(df.drop(columns=["image_path"]))
            else:
                st.dataframe(df)

            selected_timestamp = st.selectbox(
                "Select a timestamp to view image:",
                df["timestamp"].tolist()
            )

            if selected_timestamp:
                row = df[df["timestamp"] == selected_timestamp].iloc[0]

                if "image_path" in row and os.path.exists(row["image_path"]):
                    image = Image.open(row["image_path"])
                    st.image(image, caption=f"🕒 {selected_timestamp}", use_container_width=True)
                else:
                    st.warning("🕵️ This entry was created before image saving was implemented.")

            st.markdown("---")
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Diagnosis Log CSV",
                data=csv_data,
                file_name="diagnosis_log.csv",
                mime="text/csv",
            )

            if st.button("🗑️ Delete All Diagnoses"):
                os.remove(LOG_FILE)
                st.warning("🗑️ Diagnosis history deleted.")
                st.rerun()

        else:
            st.info("🕊️ No diagnoses logged yet.")
    else:
        st.info("📁 No diagnosis history found.")