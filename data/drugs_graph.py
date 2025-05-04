# gnn/data/drugs_graph.py

import dgl
import torch

DRUGS = [
    "Aspirin", "Ibuprofen", "Paracetamol", "Amoxicillin", "Atorvastatin",
    "Metformin", "Lisinopril", "Omeprazole", "Warfarin", "Simvastatin",
    "Azithromycin", "Ciprofloxacin", "Prednisone", "Albuterol", "Levothyroxine"
]

INTERACTIONS = [
    ("Aspirin", "Warfarin"),
    ("Ibuprofen", "Warfarin"),
    ("Aspirin", "Ibuprofen"),
    ("Paracetamol", "Amoxicillin"),
    ("Atorvastatin", "Simvastatin"),
    ("Azithromycin", "Ciprofloxacin"),
    ("Prednisone", "Albuterol"),
    ("Lisinopril", "Omeprazole"),
    ("Metformin", "Atorvastatin"),
]

# Build a node index
drug_to_idx = {drug: idx for idx, drug in enumerate(DRUGS)}

# Prepare edges as indices
src = [drug_to_idx[src_drug] for src_drug, _ in INTERACTIONS]
dst = [drug_to_idx[dst_drug] for _, dst_drug in INTERACTIONS]

# Create DGL Graph
def build_graph():
    # Create graph with directional edges
    g = dgl.graph((src, dst))

    # Optional: Add reverse edges (bi-directional)
    g = dgl.to_bidirected(g)

    # Initialize node features (optional for now)
    g.ndata["feat"] = torch.eye(g.num_nodes())  # Identity matrix as dummy features

    return g

if __name__ == "__main__":
    graph = build_graph()
    print(graph)
    print("Node features:", graph.ndata["feat"])
