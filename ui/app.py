# ui/app.py

from dotenv import load_dotenv
import os
import sys
import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io

# Load environment variables
load_dotenv(override=True)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.explainer import explain_diagnosis
from utils.medical_agent import get_medical_consultation

# === Streamlit Config ===
st.set_page_config(page_title="AI Medical Diagnosis Assistant", layout="centered")

# === Sidebar Navigation ===
st.sidebar.image("assets/logo.png", width=150)
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Select a page:",
    ["🩻 Upload X-ray", "📝 Symptom Consultation", "📜 View Past Diagnoses"],
)

st.sidebar.markdown(f"📍 **Current Page:** {page}")

# === Page Routing ===

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
                backend_url = os.getenv("BACKEND_URL", "http://localhost:8000/diagnose")
                response = requests.post(backend_url, files={"file": (uploaded_file.name, file_bytes, uploaded_file.type)})

                if response.status_code == 200:
                    result = response.json()

                    st.balloons()
                    st.success("✅ Diagnosis Complete!")

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
                        st.experimental_rerun()

                else:
                    st.error(f"❌ Backend Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"🚨 Request Failed: {e}")

elif page == "📝 Symptom Consultation":
    st.markdown("<h1 style='text-align: center;'>🩺 AI Medical Consultation</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Describe your symptoms and receive preliminary AI-driven medical advice. (This does not replace a doctor's consultation.)</p>", unsafe_allow_html=True)

    symptoms = st.text_area("📝 Describe your symptoms:")

    if st.button("🔍 Analyze Symptoms"):
        if symptoms.strip() == "":
            st.warning("⚠️ Please enter some symptoms.")
        else:
            with st.spinner("Analyzing your symptoms..."):
                advice = get_medical_consultation(symptoms)
                st.success("✅ Preliminary Medical Advice:")
                st.markdown(f"💬 {advice}")

elif page == "📜 View Past Diagnoses":
    st.markdown("<h1 style='text-align: center;'>📜 Diagnosis History</h1>", unsafe_allow_html=True)

    if os.path.exists("data/diagnosis_log.csv"):
        df = pd.read_csv("data/diagnosis_log.csv")

        if not df.empty:
            if "image_path" in df.columns:
                st.dataframe(df.drop(columns=["image_path"]))
            else:
                st.dataframe(df)

            selected_timestamp = st.selectbox(
                "Select a Timestamp to View Image:",
                df["timestamp"].tolist()
            )

            if selected_timestamp:
                row = df[df["timestamp"] == selected_timestamp].iloc[0]

                if "image_path" in row and os.path.exists(row["image_path"]):
                    image = Image.open(row["image_path"])
                    st.image(image, caption=f"🕒 {selected_timestamp}", use_container_width=True)
                else:
                    st.warning("🕵️ This entry was created before image saving was implemented.")
        else:
            st.info("🕊️ No diagnoses logged yet.")
    else:
        st.info("📁 No diagnosis history found.")
