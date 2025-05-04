# ui/pages/3_Consultation.py

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)
API_URL = os.getenv("API_CONSULT_URL", "http://localhost:8000/consult")

st.set_page_config(page_title="Medical Consultation", layout="centered")

st.title("🩺 AI Medical Consultation")
st.markdown(
    "Describe your symptoms to receive preliminary medical advice (⚠️ this does not replace a doctor's consultation)."
)

symptoms = st.text_area("📝 Describe your symptoms:", height=150)

if st.button("🔍 Analyze Symptoms"):
    if symptoms.strip() == "":
        st.warning("⚠️ Please enter some symptoms first.")
    else:
        with st.spinner("Consulting medical assistant..."):
            try:
                response = requests.post(API_URL, json={"symptoms": symptoms}, timeout=30)
                data = response.json()

                if response.status_code == 200:
                    if "consultation" in data:
                        st.success("✅ Consultation Complete!")
                        st.markdown("### 📄 Results")
                        st.markdown(data["consultation"])
                    elif "error" in data:
                        st.error(f"❌ API Error: {data['error']}")
                    else:
                        st.error(f"⚠️ Unexpected response: {data}")
                else:
                    st.error(f"❌ API Error {response.status_code}: {data}")

            except requests.exceptions.RequestException as e:
                st.error(f"🚨 Failed to connect to API: {e}")
