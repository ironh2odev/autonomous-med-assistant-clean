# ui/pages/3_Consultation.py

import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from utils.medical_agent import consult_symptoms

st.set_page_config(page_title="Medical Consultation", layout="centered")

st.title("🩺 AI Medical Consultation")
st.markdown("Describe your symptoms and receive preliminary medical advice (this does not replace a doctor's consultation).")

# User Input
symptoms = st.text_area("📝 Describe your symptoms:", height=150)

if st.button("🔍 Analyze Symptoms"):
    if symptoms.strip() == "":
        st.warning("⚠️ Please enter some symptoms first.")
    else:
        with st.spinner("Consulting medical assistant..."):
            consultation_result = consult_symptoms(symptoms)
            st.success("✅ Consultation Complete!")
            st.markdown("### 📄 Results")
            st.markdown(f"{consultation_result}")
