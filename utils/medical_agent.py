# utils/medical_agent.py

import openai
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

def consult_symptoms(symptoms: str) -> str:
    prompt = f"""
    You are a professional medical assistant. The patient reports:
    "{symptoms}"

    Provide:
    1. Likely diagnosis
    2. Recommended tests
    3. Initial care advice
    Remind user to see a doctor.
    Limit to 3-5 sentences.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()