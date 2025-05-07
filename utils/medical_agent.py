# utils/medical_agent.py

import openai
import os
from dotenv import load_dotenv
import torch
# from gnn.models.gnn_model import DrugGNN  # ⏸️ temporarily disabled
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

# MODEL_PATH = os.getenv("MODEL_PATH", "gnn/models/gnn_model.pt")
# GRAPH_PATH = os.getenv("GRAPH_PATH", "uploads/drugs_graph.pt")

# INPUT_DIM = int(os.getenv("INPUT_DIM", 10))
# HIDDEN_DIM = int(os.getenv("HIDDEN_DIM", 16))
# OUTPUT_DIM = int(os.getenv("OUTPUT_DIM", 2))

# model = DrugGNN(in_feats=INPUT_DIM, hidden_feats=HIDDEN_DIM, num_classes=OUTPUT_DIM)

# try:
#     model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
#     model.eval()
#     logger.info("GNN model loaded successfully.")
# except Exception as e:
#     logger.error(f"Failed to load GNN model: {e}")

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

# def check_drug_interactions(drug_ids: list[int]) -> list[dict]:  # ⏸️ temporarily disabled
#     import dgl
#     try:
#         graph_data = torch.load(GRAPH_PATH)
#         g = dgl.graph((graph_data["src"], graph_data["dst"]))
#         g.ndata["feat"] = graph_data["feat"]
#     except Exception as e:
#         raise RuntimeError(f"Graph load error: {e}")
#
#     results = []
#     for drug1 in drug_ids:
#         for drug2 in drug_ids:
#             if drug1 != drug2 and g.has_edges_between(drug1, drug2):
#                 edge_feats = g.ndata["feat"][drug1] + g.ndata["feat"][drug2]
#                 with torch.no_grad():
#                     pred = model(edge_feats.unsqueeze(0))
#                     prob = torch.softmax(pred, dim=1)[0, 1].item()
#                 results.append({
#                     "drug1": drug1,
#                     "drug2": drug2,
#                     "risk": round(prob, 4)
#                 })
#     logger.info(f"Checked interactions for IDs: {drug_ids} — Found {len(results)} interactions")
#     return results