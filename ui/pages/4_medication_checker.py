# ui/pages/4_medication_checker.py

import streamlit as st
from gnn.drug_interactions import predict_interaction

st.set_page_config(page_title="Medication Safety Checker", layout="centered")

st.markdown("<h1 style='text-align: center;'>🧪 Medication Safety Checker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Select two medications to check for potential dangerous interactions.</p>", unsafe_allow_html=True)

st.markdown("---")

# ✅ Sample drug list
drug_options = [
    "Aspirin", "Ibuprofen", "Paracetamol", "Amoxicillin", "Atorvastatin",
    "Metformin", "Lisinopril", "Omeprazole", "Warfarin", "Simvastatin",
    "Azithromycin", "Ciprofloxacin", "Prednisone", "Albuterol", "Levothyroxine"
]

# Input fields as dropdowns
drug1 = st.selectbox("💊 Select Drug 1", options=[""] + drug_options)
drug2 = st.selectbox("💊 Select Drug 2", options=[""] + drug_options)

# Check Button
if st.button("🔍 Check Interaction"):
    if not drug1 or not drug2:
        st.warning("⚠️ Please select both drugs before checking.")
    elif drug1 == drug2:
        st.info("🤔 You selected the same drug twice — no interaction detected except possible confusion!")
    else:
        with st.spinner("Analyzing drug safety..."):
            label, score = predict_interaction(drug1, drug2)

            if "Interaction" in label:
                st.error(f"🚨 {label} (Similarity: {score:.2f})")
            else:
                st.success(f"✅ {label} (Similarity: {score:.2f})")

        st.markdown("---")
        if st.button("🔄 Check Another Pair"):
            st.experimental_rerun()
