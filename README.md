# 🧠 Autonomous AI Medical Diagnosis & Treatment Recommender

This AI-powered assistant uses cutting-edge models (ViT, LLMs, GNNs, RL) to:

- Detect anomalies in medical images
- Diagnose based on symptoms using literature-backed LLMs
- Predict safe treatment options via GNNs
- Personalize treatment plans using reinforcement learning

## 🏗️ Tech Stack
- Vision Transformers (ViT)
- LLMs (MedPaLM / GPT-4 with PubMed)
- GNNs (PyTorch Geometric)
- RL (PPO / DQN)
- FastAPI + Streamlit

## 🛠️ Setup
```bash
pip install -r requirements.txt
cp .env.template .env

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/ironh2odev/autonomous-med-assistant.git
cd autonomous-med-assistant
