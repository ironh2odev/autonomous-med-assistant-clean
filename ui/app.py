# ui/app.py

from dotenv import load_dotenv
import os
load_dotenv(override=True)

import sys
import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io

# Load environment variables
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.explainer import explain_diagnosis

st.set_page_config(page_title="AI Medical Diagnosis", layout="centered")

# Sidebar navigation
page = st.sidebar.radio("🔎 Navigate", ["🩻 Upload X-ray", "🧻 View Past Diagnoses"])
st.sidebar.markdown(f"📍 You are on: **{page}**")

# Upload + Diagnosis
if page == "🩻 Upload X-ray":
    st.markdown("<h1 style='text-align: center;'>🩻 Autonomous AI Medical Diagnosis Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload a chest X-ray image to receive an AI-generated diagnosis.</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📤 Upload X-ray Image (.png, .jpg)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()

        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        st.image(image, caption="📸 Uploaded X-ray", use_container_width=True)

        st.markdown("---")
        st.markdown("<h3 style='text-align: center;'>🔬 The doctor is reviewing your X-ray...</h3>", unsafe_allow_html=True)

        with st.spinner("This may take a few seconds..."):
            try:
                backend_url = os.getenv("BACKEND_URL", "http://localhost:8000/diagnose")
                response = requests.post(
                    backend_url,
                    files={"file": (uploaded_file.name, file_bytes, uploaded_file.type)}
                )

                if response.status_code == 200:
                    result = response.json()

                    st.balloons()
                    st.success("✅ Diagnosis Complete!")

                    st.markdown(f"### 🏷️ **Diagnosis:** `{result['diagnosis']}`")
                    st.info(f"📊 **Confidence:** `{result['confidence'] * 100:.2f}%`")

                    if "note" in result:
                        st.markdown(f"🩺 _Doctor’s Note:_ {result['note']}")

                    # GPT Medical Explanation
                    st.markdown("---")
                    st.markdown("### 🧠 Medical Explanation")

                    with st.spinner("Summarizing in simple language..."):
                        explanation = explain_diagnosis(result['diagnosis'])
                        st.markdown(f"💬 _{explanation}_")

                    st.markdown("---")
                    if st.button("📤 Upload Another X-ray"):
                        st.experimental_rerun()

                else:
                    st.error(f"❌ Backend Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"🚨 Request Failed: {e}")

# View Past Diagnoses
elif page == "🧻 View Past Diagnoses":
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
