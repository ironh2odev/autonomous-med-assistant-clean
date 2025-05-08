# streamlit_app.py

import streamlit as st
import requests

API_URL = "https://autonomous-med-assistant-clean.onrender.com"

st.title("🩺 Autonomous AI Medical Assistant")

st.subheader("Symptom Consultation")
symptoms = st.text_area("Describe your symptoms:")
if st.button("Consult"):
    if symptoms.strip():
        with st.spinner("Consulting AI doctor..."):
            response = requests.post(f"{API_URL}/consult", json={"symptoms": symptoms})
            if response.status_code == 200:
                st.success(response.json().get("consultation", "No response."))
            else:
                st.error("Failed to get consultation.")
    else:
        st.warning("Please enter some symptoms.")