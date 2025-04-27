# utils/explainer.py

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_diagnosis(diagnosis: str) -> str:
    """Call OpenAI to generate a medical explanation for a diagnosis."""
    prompt = f"""
    You are a helpful medical assistant. Explain why a chest X-ray might be diagnosed as "{diagnosis}".
    Use professional radiology reasoning. Keep the explanation concise (2–3 sentences).
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # You can change to "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant specialized in radiology."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=200,
        )
        explanation = response.choices[0].message.content.strip()
        return explanation

    except Exception as e:
        return f"❌ Request Failed:\n\n{e}"
