# utils/medical_agent.py

import openai
import os
from dotenv import load_dotenv

load_dotenv(override=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

def consult_symptoms(symptoms: str) -> str:
    """
    Given user symptoms, return a probable diagnosis, recommended tests, and advice.
    """
    prompt = f"""
    You are a highly experienced medical assistant. A user reports the following symptoms:
    
    "{symptoms}"

    Based on this, provide:
    1. The most likely diagnosis.
    2. Recommended medical tests or imaging.
    3. Initial care advice (home care if appropriate).
    
    Always remind the user to consult a licensed physician for a proper examination.
    Be concise, professional, and easy to understand (3-5 sentences max).
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=300,
    )

    output = response["choices"][0]["message"]["content"].strip()
    return output
