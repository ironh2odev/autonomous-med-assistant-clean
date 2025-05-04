# ui/pages/4_medication_checker.py

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)
API_URL = os.getenv("API_CHECK_DRUG_URL", "http://localhost:8000/check-drug-safety")

st.set_page_config(page_title="Medication Safety Checker", layout="centered")

st.markdown("<h1 style='text-align: center;'>🧪 Medication Safety Checker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Select two medications to check for potential dangerous interactions.</p>", unsafe_allow_html=True)
st.markdown("---")

drug_options = [
    "Aspirin", "Ibuprofen", "Paracetamol", "Amoxicillin", "Atorvastatin",
    "Metformin", "Lisinopril", "Omeprazole", "Warfarin", "Simvastatin",
    "Azithromycin", "Ciprofloxacin", "Prednisone", "Albuterol", "Levothyroxine"
]

drug1 = st.selectbox("💊 Select Drug 1", options=[""] + drug_options)
drug2 = st.selectbox("💊 Select Drug 2", options=[""] + drug_options)

if st.button("🔍 Check Interaction"):
    if not drug1 or not drug2:
        st.warning("⚠️ Please select both drugs before checking.")
    elif drug1 == drug2:
        st.info("🤔 You selected the same drug twice — no interaction detected.")
    else:
        with st.spinner("Analyzing drug safety..."):
            try:
                drug_ids = [drug_options.index(drug1), drug_options.index(drug2)]
                response = requests.post(API_URL, json={"drug_ids": drug_ids})
                if response.status_code == 200:
                    interactions = response.json().get("interactions", [])
                    if interactions:
                        risk = interactions[0]["risk"]
                        if risk > 0.5:
                            st.error(f"🚨 Interaction risk detected! Risk: {risk:.2f}")
                        else:
                            st.success(f"✅ No major interaction detected. Risk: {risk:.2f}")
                    else:
                        st.success("✅ No direct interaction found.")
                else:
                    error_msg = response.json().get('error', 'Unknown error')
                    st.error(f"❌ API Error: {error_msg}")
            except Exception as e:
                st.error(f"⚠️ Failed to contact backend: {e}")

    st.markdown("---")
    if st.button("🔄 Check Another Pair"):
        st.experimental_rerun()
