# gnn/drug_interactions.py

import torch
import torch.nn as nn
import networkx as nx
import dgl
from dgl.nn import GraphConv

# === Step 1: Create Fake Drug Graph (Just for now as a placeholder) ===
def create_graph():
    graph = nx.Graph()

    # Add drug nodes
    drugs = ["DrugA", "DrugB", "DrugC", "DrugD"]
    for drug in drugs:
        graph.add_node(drug)

    # Add edges (interactions)
    graph.add_edge("DrugA", "DrugB")  # interaction
    graph.add_edge("DrugB", "DrugC")  # interaction
    graph.add_edge("DrugC", "DrugD")  # interaction
    # No edge between DrugA and DrugD (safe)

    return graph

graph_nx = create_graph()
graph_dgl = dgl.from_networkx(graph_nx)

# === Step 2: Define a Simple GNN Model ===
class DrugInteractionModel(nn.Module):
    def __init__(self, in_feats, hidden_size, num_classes):
        super(DrugInteractionModel, self).__init__()
        self.conv1 = GraphConv(in_feats, hidden_size)
        self.conv2 = GraphConv(hidden_size, num_classes)

    def forward(self, g, features):
        h = self.conv1(g, features)
        h = torch.relu(h)
        h = self.conv2(g, h)
        return h

# Create a fake embedding for each drug (just 2 features)
drug_features = {
    "DrugA": torch.tensor([1.0, 0.0]),
    "DrugB": torch.tensor([0.0, 1.0]),
    "DrugC": torch.tensor([1.0, 1.0]),
    "DrugD": torch.tensor([0.5, 0.5]),
}
features = torch.stack([drug_features[drug] for drug in graph_nx.nodes])

# Initialize model
model = DrugInteractionModel(in_feats=2, hidden_size=4, num_classes=2)

# Dummy training (optional) – for now, let's assume random weights.

# === Step 3: Predict Interaction Between Two Drugs ===
def predict_interaction(drug1, drug2):
    drug_list = list(graph_nx.nodes)

    if drug1 not in drug_list or drug2 not in drug_list:
        return "Unknown Drugs", 0.0

    idx1 = drug_list.index(drug1)
    idx2 = drug_list.index(drug2)

    with torch.no_grad():
        logits = model(graph_dgl, features)
        score1 = logits[idx1]
        score2 = logits[idx2]
        interaction_score = torch.cosine_similarity(score1.unsqueeze(0), score2.unsqueeze(0)).item()

    if graph_nx.has_edge(drug1, drug2):
        label = "⚠️ Interaction Detected!"
    else:
        label = "✅ No Interaction (Safe)"

    return label, interaction_score
